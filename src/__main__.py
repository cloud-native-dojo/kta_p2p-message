from modules.nodes.node import Node
from modules.posts.post import Post
from random import randint, choice
import time

def main():
    # 10個のノードを作成
    nodes = [Node() for _ in range(10)]
    
    # 投稿用のサンプルコンテンツ
    titles = ["こんにちは", "ニュース", "アップデート", "重要なお知らせ", "お知らせ"]
    contents = ["世界！", "今日の天気", "新機能について", "明日の会議", "これをチェック"]
    
    # ランダムな投稿をシミュレート（50回繰り返し）
    for _ in range(50):
        # ランダムにノードを選択して投稿を作成
        posting_node = choice(nodes)
        if posting_node.is_online():  # ノードがオンラインの場合のみ投稿
            title = choice(titles)
            content = choice(contents)
            posting_node.create_post(title, content)
            print(f"ノード {posting_node.get_id()} が投稿を作成: {title}")
        
        # ランダムな同期
        if randint(1, 4) == 1:  # 25%の確率で同期を実行
            syncing_node = choice(nodes)
            syncing_node.sync_posts()
            print(f"ノード {syncing_node.get_id()} が同期を実行")
        
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
    main()