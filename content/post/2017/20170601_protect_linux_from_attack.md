---
title: Linux を安心して運用するために(Debianを例に)
date: 2017-06-01T11:33:00+09:00
slug: '1133'
aliases:
  - 1133.html
categories:
  - blog
tags:
  - linux
draft: true
---


## やること

* 意図しないアクセスを防ぎたい
    * Firewall の設定
    * fail2ban
    * SSH のパスワード認証の拒否
    * SELinux
* 攻撃の未然防止をしたい
    * 脆弱性スキャン
        * vuls
        * debsecan
    * 設定のチェック
        * lynis
* ウイルスを検知したい
    * Antivirusソフトウェアの実行
* 攻撃を受けたことに気づきたい
    * rootkit 対策(rkhunter, chkrootkit)
    * auditd
    * tripwire
    * 気休め系: debsums, etckeeper
* 設定が悪くないかを見ておきたい
    * OpenSCAP
        * Debian ではまだ unstable にしかないし、今回はやらない
        * ポリシーもRHELの方がサポートされているらしい
        * https://wiki.debian.org/UsingSCAP

## 実行環境

```
$ uname -a
Linux workdebian 4.9.0-3-amd64 #1 SMP Debian 4.9.25-1 (2017-05-02) x86_64 GNU/Linux
```

## やったこと

### clamav

```
$ sudo apt install clamav clamav-daemon
$ sudo chmod o+w /etc/clamav/freshclam.conf
$ sudo vim /etc/clamav/freshclam.conf
- DatabaseMirror db.local.clamav.net
+ DatabaseMirror db.jp.clamav.net
$ sudo chmod o-w /etc/clamav/freshclam.conf
$ sudo systemctl restart clamav-freshclam
$ sudo vim /etc/clamav/clamd.conf
$ sudo systemctl restart clamav-daemon
```

### etckeeper

```
$ sudo apt install etckeeper
```

何か変更した時
```
$ cd /etc/
$ sudo git status
$ sudo git commit -am "foo bar"
```

どこかに push しておくと便利だと思うけど、今回はやらない。

### rkhunter

```
$ sudo apt install rkhunter
```

定義ファイルの更新
```
$ sudo rkhunter --update
$ sudo rkhunter --propupd
```

スキャン
```
$ sudo rkhunter -c --sk --rwo
Warning: Hidden directory found: /etc/.java
Warning: Hidden directory found: /etc/.git
Warning: Hidden file found: /etc/.etckeeper: ASCII text
Warning: Hidden file found: /etc/.gitignore: ASCII text
sudo rkhunter -c --sk --rwo  9.45s user 7.24s system 28% cpu 57.817 total
```

Warningの修正(このWarningの内容は問題ないので、次回以降表示したくない)
```
$ sudo vim /etc/rkhunter.conf
- #ALLOWHIDDENDIR=/etc/.java
- #ALLOWHIDDENDIR=/etc/.git
+ ALLOWHIDDENDIR=/etc/.java
+ ALLOWHIDDENDIR=/etc/.git
...
- #ALLOWHIDDENFILE=/etc/.gitignore
- #ALLOWHIDDENFILE=/etc/.etckeeper
+ ALLOWHIDDENFILE=/etc/.gitignore
+ ALLOWHIDDENFILE=/etc/.etckeeper
```

### Lynis

```
$ sudo apt install lynis
```

スキャン
```
$ sudo lynis audit system --verbose
```

cronの設定
https://cisofy.com/documentation/lynis/#cronjobs に記載されているとおり、 `--cronjobs` をつけるらしい。

### auditd

```
$ sudo apt install auditd
```

### debsums, debsecan

```
$ sudo apt install debsums debsecan
```

### vuls
