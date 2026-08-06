import time
import concurrent.futures
import specialist

# 分析するレビュー。実際には別ファイルからの読み込む
my_reviews = [
    {"id": 1, "text":"このカメラは画質が素晴らしく、バッテリーも長持ちします。ただし重いのが難点です。"},
    {"id": 2, "text":"値段の割に品質が低い。1ヶ月で壊れました。サポートも最悪でした。"},
    {"id": 3, "text":"普通の商品です。特別良くも悪くもありません。価格相応だと思います。"},
]

# サブエージェントに渡す処理
def analyze_review(review):
    """一件のレビューを専門家サブエージェントで分析する"""
    my_question = f"このレビューーの感情（ポジティブ/ネガティブ/ニュートラル）と主なポイントを分析してください：\n{review['text']}"
    my_result = specialist.run("感情分析・レビュー評価", my_question)
    return {"id": review["id"], "result": my_result}


# 順次処理
def run_sequential():
    print("\n【順次処理】")
    start = time.time()
    
    my_results = []
    for review in my_reviews:
        print(f"  分析中... レビュー#{review['id']}")
        my_result = analyze_review(review)
        print(f"  #{my_result['id']}: {my_result['result'][:80]}...")
        my_results.append(my_result)
        
    elapsed = time.time() - start
    print(f" 完了：{elapsed: .1f}秒")
    return my_results

# 並列処理
def run_parallel():
    print("\n【並列処理】")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        my_futures = {
            executor.submit(analyze_review, review): review["id"]
            for review in my_reviews
        }
        my_results = []
        for future in concurrent.futures.as_completed(my_futures):
            review_id = my_futures[future]
            my_result = future.result()
            print(f" 完了：レビュー#{review_id}")
            print(f"  #{my_result['id']}: {my_result['result'][:80]}...")
            my_results.append(my_result)
            
    elapsed = time.time() - start
    print(f" 完了：{elapsed:.1f}秒")
    return my_results

# 実行
if __name__ == "__main__":
    run_sequential()
    run_parallel()