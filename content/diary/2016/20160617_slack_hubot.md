Title: 会社にslack入ったので、色々やってた
Date: 2016-06-16 14:45
Category: blog
Tags: slack, hubot

[TOC]

勤務先の会社に今日(2016/06/16)から真面目にSlackが導入されたので、やった設定をメモしておく。

# 現在のチャンネル構成

* 定常系
    * 分報用のチャンネル。個々人が作る
    * 部署用
    * チーム用
    * プロジェクト用
* 雑多な情報共有用
    * ニュース用
* トラブル用
* その他
    * 臨時に必要になるとか
    * テストとか

# やったことメモ

## RSS を Slack に移行

live dwango reader をずっと使っていたのだけど、更新頻度がそこそこで、重要度の高いRSSを Slack で追いかけることにした。

### やり方

追加自体は簡単で、通知をしてほしいチャンネルで、以下のようなコマンドを打つ。

```
# 通知したいチャンネルで入力
/feed <feed url>
```

こうしておくと、更新された時に、チャンネルに通知が来る。

### コメント

通知先のチャンネルについては、内容に応じて分けておいた方が良いと思う。
今まで自分はRSSを読んで、チームで共有するものは個別に共有していたけど、そういう情報源はチームのチャンネルに入れてしまった。
もしかしたら、別途チームのニュースチャンネルを作った方が良いかもしれない。
以下のような場合分けにした。

* 更新頻度が高すぎる
    * RSS のまま
    * そのうち、botでサマライズするように変える予定
    * 後述する通り、「RSSを読もう」という remind をしている
* 更新頻度がそこそこ
    * 共有したい
        * チーム・プロジェクト用のチャンネルへ通知
    * 自分だけで良い
        * 分報用チャンネルへ通知
        * 分報用チャンネルはオープンなので、近くのチームの人は入っているので、興味があれば見る人もいるので、RSSよりは良い

## 予定を remind する

例えば、新人の日報を見る、とか、毎日RSSを見るとかの予定を Slack で通知させることにした。
他に、そのうちやろうと思っている短い個人作業(5分以内とかのレベル)のタスクも、面倒なので、言われたその場で、 remindに入れてしまっている。

### やり方

```
# 自分用 : 平日は毎日19:00 に "<リマインド>"をする
/remind #<分報用チャンネル> to "<リマインド>" at 17:00 every weekday
# チーム用 : 月曜日は毎日19:00 に "<リマインド>"をする
/remind #<チームチャンネル> to "<リマインド>" at 10:00 every Monday
```

### コメント

```
/remind me ...
```
としても、リマインドできるけど、その場合、プライベートチャットでリマインドされる。
会社のタスクだったり、予定だったりするので、特にプライベートでやる意味がないので、チャンネルに通知することにしている。

他の使い方については、helpを見よう。 よく使いそうなのは、 `in` とかだと思う。

```
/remind help
```
## 実行に時間がかかるコマンドの終了通知

検証などで、 ansibleやらを実行するときに、時間がかかるステップがある。(例えば、windwos update。)
実行中は他の作業をしたいので、終了を通知されるようにした。

### やり方

* Slack 側 : incoming webhook を設定。
    * アイコンは、スクリプト側で指定するので、無視して良い。
    * URLをメモするのと、通知先のチャンネル、ユーザー名を決めておく程度。
* zsh shell側 : [時間がかかるコマンドの実行結果をSlackに通知する](http://qiita.com/izumin5210/items/c683cb6addc58cae59b6) を参考にした。
    * `SLACK_WEBHOOK_URL` をメモしたURL
    * `SLACK_USER_NAME` をメンションしたいユーザー名

### コメント

これは分報用チャンネルに入れた。

## GitLab, Jenkins との連携

Merge Requestが来たときとか。
やり方は、割愛。

### コメント

今のところは、複雑なことはやっていない。
また細かい設定をしたら、書く。

## Zabbix などの監視

やった。
ひとまず、alert の発生と収束だけを通知している。
slackから操作できるようにしたいが、まだやっていない。

## Redmine/JIRA 連携

これからやるけど、全社共通のものなので、Redmine 側には pluginは入れてくれないかもしれない。
botでやろうかと思っている。

## Office 365

できていない。
メール・カレンダーは連携したい。
社内ADと連携しているはずなので、社内ADの認証を通してから、APIを叩くbotを作る必要があると思っている。
でも、APIのたたき方がわからない。まだ調べる気が起きていない。

### 暫定対処

直接は連携できていないが、ひとまず、メールをSlackに転送するようにした。

## bot

まだ書いてない。
これから書く。ひとまず、以下のあたりをやるつもり。

* 打刻
* 定時頃になったら、今月の残業時間を通知
* Redmine連携
