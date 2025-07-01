![logo](./img/redis_logo.png)

# はじめに
Redisの検証用リポジトリ
Redisとは、**インメモリ型データストア**と呼ばれる超高速なDBである。

メモリ上にデータを保持することで、超高速な読み書きが可能となる。

一般席な用途は、キャッシュ、セッション管理、ジョブキューなど。

本リポジトリでは、Redisの実装方法及び、基本的な利用方法・実装前後の速度テストを行う。

# 参考文献

[Redis Official Document](https://redis.io/docs/latest/develop/)

# Redisの実装

基本的には、Dockerコンテナ上で起動する。

最も基本的な形で起動するので、[docker-compose.yaml](./docker-compose.yaml)を参照。

```
[実行コマンド]
docker compose -f docker-compose.yaml up -d

[結果]
[+] Running 8/8
 ✔ redis Pulled                                                                                                                             13.5s 
   ✔ 3da95a905ed5 Pull complete                                                                                                              7.8s 
   ✔ db655ba2dcca Pull complete                                                                                                              7.9s 
   ✔ 4ef8fa7693bb Pull complete                                                                                                              7.9s 
   ✔ 881b4a6fb2ec Pull complete                                                                                                              8.6s 
   ✔ 6d7393f5b310 Pull complete                                                                                                              8.7s 
   ✔ 4f4fb700ef54 Pull complete                                                                                                              8.8s 
   ✔ ab22bb3606ca Pull complete                                                                                                              8.9s 
[+] Running 2/2
 ✔ Network redis_default   Created                                                                                                           0.4s 
 ✔ Container redis-server  Started    

[確認コマンド]
docker ps

[結果]
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                       NAMES
7c80364bd246   redis     "docker-entrypoint.s…"   57 seconds ago   Up 54 seconds   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   redis-server
```

Redisサーバが立ち上がった。

# ローカルPC側

## Pythonの仮想環境を準備
ターミナルで、プロジェクト用のディレクトリに移動してから以下を実行する。

`C:\Users\[ユーザ名]\Python`ディレクトリを作成して、そこに仮想環境を作成する。

```
[実行コマンド]
python -m venv venv

[確認コマンド]
ls

[結果]
    Directory: C:\Users\[ユーザ名]\Python

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          2025/07/01    14:13                venv
```

ディレクトリに移動する。

```
[実行コマンド]
cd .\venv\

```

ここからは2通りの方法がある。
1つ目は、仮想環境をアクティベートしてから使う方法。2つ目は、仮想環境内のディレクトリを直接していしてコマンドを実行する方法である。

自分は後者の方が好みなのでそちらを採用する。

```
[実行コマンド]
.\Scripts\pip.exe list

[結果]
Package Version
------- -------
pip     25.0.1
```

Pythonで利用するRedisパッケージのインストール

```
[実行コマンド]
 .\Scripts\pip.exe install redis

[結果]
Collecting redis
  Downloading redis-6.2.0-py3-none-any.whl.metadata (10 kB)
Downloading redis-6.2.0-py3-none-any.whl (278 kB)
Installing collected packages: redis
Successfully installed redis-6.2.0
```

Redisの6.2.0がインストールされた。

## Pythonコードの実行

[Pythonコード](./test_redis.py)を仮想環境の中にコピーし、接続情報を書き換える。


今回の場合、接続先ホストのIPアドレスは`192.168.56.129`である。

仮想環境内のPythonコードで実行する。


```
[実行コマンド]
.\Scripts\python.exe .\test_redis.py

[結果]
▶ DBから取得
Value-for-user123
1回目： 1.017745018005371 秒

▶ キャッシュから取得
Value-for-user123
2回目： 0.007069826126098633 秒
```

もう一度同じコマンドを打つ。
```
[実行コマンド]
.\Scripts\python.exe .\test_redis.py

[結果]
▶ キャッシュから取得
Value-for-user123
1回目： 0.013982295989990234 秒
▶ キャッシュから取得
Value-for-user123
2回目： 0.0034804344177246094 秒
```

## コード解説

接続先情報設定部分
```
r = redis.Redis(host='localhost', port=6379, db=0)
```
`db=0`について、Redisには「DB番号(0〜15)」があり、ここでは0番を使っている

```
get_data("user123")
```

1.Redisに user123 というキーがあるかを確認 → `r.exists("user123")`

2.なければ「疑似DBアクセス」（time.sleep(1)で遅延）→ `Value-for-user123` という値を生成

3.その値をRedisにセット → `r.set("user123", value)`

4.次回のアクセスでは Redis から即座に取得 → `r.get("user123")`

Redisのget命令は、`r.get(key)`でPythonのRedisライブラリが内部的に Redisプロトコル を使って、`GET user123`というコマンドを TCPポート6379でRedisに送信している。

# Redis側のKVを確認


Redisコンテナに入る
```
docker exec -it redis-server redis-cli

127.0.0.1:6379> 
```

キーの一覧を取得
```
keys *
1) "user123"
127.0.0.1:6379> 
```

特定のキーの中身を見る

get user123

"Value-for-user123"

他にも以下のようなコマンドがある
キーがあるか確認
```
exists mykey	1（あり）or 0（なし）
```
削除
```
del mykey	指定キーを削除
```
全削除（注意）
```
flushall	すべてのデータを削除（注意）
```

# 活動への応用