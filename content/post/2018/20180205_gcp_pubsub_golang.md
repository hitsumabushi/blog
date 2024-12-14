---
title: Google Cloud Pub/Sub をGolangから使おうとしてハマったことまとめ
date: 2018-02-05T20:09:00+09:00
slug: '2009'
markup.goldmark.renderer.unsafe: true
categories:
  - blog
tags:
  - GCP
  - golang
---


# 概要

[Google Pub/Sub](https://cloud.google.com/pubsub/overview?hl=ja) を [GoのSDK](https://github.com/GoogleCloudPlatform/google-cloud-go) から使おうとしていました。
やっているといくつか詰まったので、メモしておきます。

1. サービスアカウントを利用するためにCredentials JSONを指定する
2. サブスクリプションの `Pub/Sub サブスクライバー権限` を与えても Permission Denied になる

## サービスアカウントを利用するためにCredentials JSONを指定する

権限の都合上、サービスアカウントのCredentials JSONを利用して認証したい、という要件がありました。
ドキュメントを見ていると、 [ADC(Application Default Credentials)](https://cloud.google.com/docs/authentication/production?hl=ja) を利用して認証している場合が多いです。
これを使う場合、 `GOOGLE_APPLICATION_CREDENTIALS` という環境変数が設定されていれば、そのファイルを読んでくれるのですが、今回の要件では複数の Credentials を利用したかったので、Go プログラム中で指定する必要がありました。

結論としては、以下のような形でpubsub client を作るときに認証情報を渡すことができます。

```
  jsonKey, err := ioutil.ReadFile(credentialJSONPath)
  conf, err := google.JWTConfigFromJSON(jsonKey, pubsub.ScopePubSub, pubsub.ScopeCloudPlatform)
  if err != nil {
    log.Fatal(err)
  }
  ctx := context.Background()
  ts := conf.TokenSource(ctx)
  c, err := pubsub.NewClient(ctx, projectID, option.WithTokenSource(ts))
```

Publisherのサンプルは以下の通りです。

<script src="https://gist.github.com/hitsumabushi/7cf1fa45813208f314b29da84a3ff2cc.js"></script>

## サブスクリプションの `Pub/Sub サブスクライバー` 権限を与えても Permission Denied になる

結論としては、 `Pub/Sub サブスクライバー` 権限に加えて、 `Pub/Sub 閲覧者` の権限が必要でした。
ドキュメント上は、 `Pub/Sub サブスクライバー` 権限だけで良さそうに見えますが、権限不足だったようでした。
Subscriberのサンプルは以下の通りです。

<script src="https://gist.github.com/hitsumabushi/baaeefd241e27ab0414763bdc6a93f11.js"></script>
