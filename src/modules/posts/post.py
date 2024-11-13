from uuid import UUID, uuid4


class Post:
    """
    ポストクラス
    あまり重要ではないので、簡略化している
    """
    posts = []

    def __init__(self, title:str, content:str) -> None:
        self.__id: UUID = uuid4()
        self.__title = title
        self.__content = content
        self.__class__.posts.append(self)

    # 基本的なデータ操作
    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_content(self):
        return self.__content
    
    def get_post_data(self):
        return {
            "id": self.__id,
            "title": self.__title,
            "content": self.__content
        }

    @classmethod
    def get_all(cls):
        """
        Postクラスが持っている全てのポストを取得する
        """
        return cls.posts
    
    @classmethod
    def get_count_all(cls):
        """
        Postクラスが持っている全てのポスト数を取得する
        """
        return len(cls.posts)
    
    @classmethod
    def reset_class(cls):
        """
        Postクラスが持っている全てのポストを削除する
        """
        cls.posts = []
    