"""deta exchangeのメインスクリプト
このモジュールは分散型メッセージングシステムのシミュレーションを実行します。
複数のノード間での投稿の作成と同期をシミュレートします。
定数:
    DEFAULT_NODE_COUNT (int): デフォルトのノード数
    DEFAULT_MAX_POSTS (int): デフォルトの最大投稿数
    DEFAULT_SYNC_PROBABILITY (float): デフォルトの同期確率
関数:
    main(node_count=5, max_posts=10, sync_probability=0.25): 
        シミュレーションのメインロジックを実行します。
        Args:
            node_count (int): シミュレーションで使用するノードの数
            max_posts (int): 作成する投稿の最大数
            sync_probability (float): 各ステップで同期が発生する確率（0.0～1.0）
        出力:
            - 投稿の作成と同期のリアルタイムログ
            - 各ノードの投稿カバー率の統計
            - 各ノードの通信回数と投稿数の最終統計
"""

from modules.nodes.node import Node
from modules.posts.post import Post
from random import randint, choice
import time

# 定数の定義
DEFAULT_NODE_COUNT = 10
DEFAULT_MAX_POSTS = 50
DEFAULT_SYNC_PROBABILITY = 0.25
DEFAULT_PRINT_OUTPUT = True
DEFAULT_USE_SLEEP = True

def main(node_count=DEFAULT_NODE_COUNT, max_posts=DEFAULT_MAX_POSTS, sync_probability=DEFAULT_SYNC_PROBABILITY, print_output=DEFAULT_PRINT_OUTPUT, use_sleep=DEFAULT_USE_SLEEP):
    nodes = [Node() for _ in range(node_count)]
    titles = ["タイトル1", "タイトル2", "タイトル3"]
    contents = ["内容1", "内容2", "内容3"]

    for _ in range(max_posts):
        posting_node = choice(nodes)
        if posting_node.is_online():  # ノードがオンラインの場合のみ投稿
            title = choice(titles)
            content = choice(contents)
            posting_node.create_post(title, content)
            if print_output:
                print(f"ノード {posting_node.get_id()} が投稿を作成: {title}")
        
        # ランダムな同期
        if randint(1, 100) <= sync_probability * 100:  # sync_probabilityの確率で同期を実行
            syncing_node = choice(nodes)
            syncing_node.sync_posts()
            if print_output:
                print(f"ノード {syncing_node.get_id()} が同期を実行")
        
        if use_sleep:
            time.sleep(0.1)  # より現実的な動作のための小さな遅延
    
    # 総投稿数をPostクラスメソッドから取得
    total_posts = Post.get_count_all()

    # 投稿カバー率の統計を表示
    print("\n=== 投稿カバー率 ===")
    for node in nodes:
        posts_count = len(node.get_posts())
        coverage_percent = (posts_count / total_posts * 100) if total_posts > 0 else 0
        print(f"ノード {node.get_id()}: {posts_count}/{total_posts} 投稿 ({coverage_percent:.1f}%)")

    # 最終統計を表示
    print("\n=== 最終統計 ===")
    total_communications = 0
    
    for node in nodes:
        comm_count = node.communication_count
        total_communications += comm_count
        print(f"ノード {node.get_id()}: 通信回数 {comm_count}回, 投稿数 {node.get_post_count()}件")
    
    print(f"\n全ノードの総通信回数: {total_communications}")

if __name__ == "__main__":
    try:
        node_count = int(input(f"ノード数を入力してください (デフォルト: {DEFAULT_NODE_COUNT}): ") or DEFAULT_NODE_COUNT)
        max_posts = int(input(f"最大投稿数を入力してください (デフォルト: {DEFAULT_MAX_POSTS}): ") or DEFAULT_MAX_POSTS)
        sync_probability = float(input(f"同期を行う確率を入力してください (デフォルト: {DEFAULT_SYNC_PROBABILITY}): ") or DEFAULT_SYNC_PROBABILITY)
        print_output = input(f"出力を表示しますか？ (デフォルト: {DEFAULT_PRINT_OUTPUT}) [y/n]: ").lower() in ['y', 'yes', '']
        use_sleep = input(f"遅延を使用しますか？ (デフォルト: {DEFAULT_USE_SLEEP}) [y/n]: ").lower() in ['y', 'yes', '']
    except ValueError:
        print("入力が無効です。デフォルト値を使用します。")
        node_count = DEFAULT_NODE_COUNT
        max_posts = DEFAULT_MAX_POSTS
        sync_probability = DEFAULT_SYNC_PROBABILITY
        print_output = DEFAULT_PRINT_OUTPUT
        use_sleep = DEFAULT_USE_SLEEP

    main(node_count, max_posts, sync_probability, print_output, use_sleep)