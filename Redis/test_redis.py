import redis
import time

# Redisに接続（ローカルホスト:6379）
r = redis.Redis(host='192.168.56.129', port=6379, db=0)

def get_data_from_db(key):
    time.sleep(1)  # 擬似的に重い処理
    return f"Value-for-{key}"

def get_data(key):
    if r.exists(key):
        print("▶ キャッシュから取得")
        return r.get(key).decode()
    print("▶ DBから取得")
    value = get_data_from_db(key)
    r.set(key, value)
    return value

# 実行テスト
start = time.time()
print(get_data("user123"))
print("1回目：", time.time() - start, "秒")

start = time.time()
print(get_data("user123"))
print("2回目：", time.time() - start, "秒")
