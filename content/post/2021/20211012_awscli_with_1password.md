---
title: 1Password CLIを使ってTOTPを取得する
date: 2021-10-12T01:00:00+09:00
slug: '0100'
aliases:
  - 0100.html
categories:
  - blog
tags:
  - aws
  - 1password
---


2要素認証を必須にしたAWSのswitch roleで、temporary credentialsをCLIで取得したかった。
TOTPの数字を毎回調べるのが面倒で、簡単にできないか調べたところ、1Password CLIというのがあった。1Passwordユーザなので、これを利用する。
ただし、当然のことだが、2要素認証のデバイスとして、1Passwordが利用されている状況とする。

## 1Password CLIの初期設定

1Password CLI を利用できるようにする。
[1Password CLIのGetting Started](https://support.1password.com/command-line-getting-started/)を見て、初期設定する。

```sh
$ op signin _1password_url_ _signin_address_
... # Secret Key, Password, (設定していればTOTPの6-digit)を聞かれる
```
短縮形が `_1password_url_` から自動的に決まるが、どうしても指定したい場合には、 `--shorthand`オプションで指定する。

## TOTPの取得

通常の1password appのように、30minアクセスがなければ、ロックされるため、パスワードの入力が必要。
1passwordのURLが `example.1password.com` であれば、
```sh
$ eval $(op signin example)
```
として、再認証する。
環境変数 `OP_SESSION_example` に認証したときのsession情報が載る。(`--session` オプションで各コマンドごとに渡しても良い)

TOTPを取得するには、以下のコマンドを実行する。
```sh
$ op get totp "UUID or Name"
```
UUIDで指定したい場合には、 `op list items --categories Login` の結果をjqなどで調べて、取得する。

## 終わり

以上で概ねやりたかった、CLIでTOTPを取得することができるようになった。
最近1PasswordはLinux Desktop向けのアプリを出していたりしているので、もう少し真面目に使っていきたい所存。

ちなみに、複数のプロファイルの切り替えなどで便利なように、 [99designs/aws-vault](https://github.com/99designs/aws-vault)というのもあるらしいが、特に使わずに自前シェルスクリプトで使っている。