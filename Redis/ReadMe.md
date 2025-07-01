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


[確認コマンド]
docker ps

[結果]

```