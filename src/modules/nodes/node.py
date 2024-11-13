from random import randint
from uuid import UUID

from modules.posts.post import Post
from modules.dns.dns import Dns


class Node:
    """
    ノードクラス
    主にここを変更する
    """

    nodes = []
    ONLINE_PROBABILITY = 0.8  # 80% chance of being online

    def __init__(self) -> None:
        self.__id = len(self.__class__.nodes)
        self.__posts = {}
        self.__post_count = 0  # 各ノードが何件投稿したかを保持する変数
        self.communication_count = 0
        self.__class__.nodes.append(self)
        Dns.add_node(self)

    def is_online(self):
        return randint(1, 100) <= self.ONLINE_PROBABILITY * 100

    def get_id(self):
        return self.__id

    def create_post(self, title: str, content: str):
        post = Post(title, content)
        self.__posts[post.get_id()] = post.get_post_data()
        self.__post_count += 1  # 投稿数をインクリメント
        self.broadcast_post(post)
        return post

    def receive_post(self, post_data: dict):
        if self.is_online():
            post_id = UUID(post_data["id"]) if isinstance(
                post_data["id"], str) else post_data["id"]
            self.__posts[post_id] = post_data
            return True
        return False

    def broadcast_post(self, post: Post):
        recipients = [node for node_id,
                      node in Dns.node_dict.items() if node_id != self.__id]
        self.communication_count += len(recipients)
        for node in recipients:
            node.receive_post(post.get_post_data())

    def send_post_order_log_m(self, post: Post):
        node_ids = list(Dns.node_dict.keys())
        node_count = len(node_ids)
        start_index = node_ids.index(self.__id)
        loop_completed = False

        recipients = []
        step = 2  # 2の自乗分離れるステップ

        for i in range(1, node_count):
            target_index = (start_index + step ** i) % node_count
            if target_index < start_index:
                loop_completed = True
            if loop_completed and node_ids[target_index] >= self.__id:
                break
            recipients.append(Dns.node_dict[node_ids[target_index]])

        for node in recipients:
            self.communication_count += 1
            node.receive_post(post.get_post_data())

    def sync_posts(self):
        if self.is_online():
            for node_id, node in Dns.node_dict.items():
                if node_id != self.__id:
                    self.communication_count += 1
                    posts_copy = node.__posts.copy()
                    for post_id, post_data in posts_copy.items():
                        if post_id not in self.__posts:
                            self.__posts[post_id] = post_data
                            # 直接post_dataを使用して他のノードと共有
                            recipients = [n for nid, n in Dns.node_dict.items()
                                          if nid != self.__id and nid != node_id]
                            self.communication_count += len(recipients)
                            for recipient in recipients:
                                recipient.receive_post(post_data)

    def sync_posts_order_log_m(self):
        if self.is_online():
            node_ids = list(Dns.node_dict.keys())
            node_count = len(node_ids)
            start_index = node_ids.index(self.__id)

            for node_id, node in Dns.node_dict.items():
                if node_id != self.__id:
                    self.communication_count += 1
                    posts_copy = node.__posts.copy()
                    for post_id, post_data in posts_copy.items():
                        if post_id not in self.__posts:
                            self.__posts[post_id] = post_data
                            # 直接post_dataを使用して他のノードと共有
                            recipients = []
                            step = 2  # 2の自乗分離れるステップ
                            loop_completed = False

                            for i in range(1, node_count):
                                target_index = (
                                    start_index + step ** i) % node_count
                                if target_index < start_index:
                                    loop_completed = True
                                if loop_completed and node_ids[target_index] >= self.__id:
                                    break
                                recipients.append(
                                    Dns.node_dict[node_ids[target_index]])

                            for recipient in recipients:
                                self.communication_count += 1
                                recipient.receive_post(post_data)

    def get_posts(self):
        return self.__posts

    def get_post_count(self):
        return self.__post_count
