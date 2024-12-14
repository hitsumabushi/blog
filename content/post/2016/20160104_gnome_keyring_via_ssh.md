---
title: WIP - GitをHTTPSで利用するときに、パスワードを記憶させておく via SSH
date: 2016-01-04T14:37:00+09:00
slug: '1437'
aliases:
  - 1437.html
categories:
  - blog
tags:
  - git
draft: true
---


*まだ設定できていない*

## 参考

- <https://www.kernel.org/pub/software/scm/git/docs/v1.7.9/gitcredentials.html>
- <http://stackoverflow.com/questions/5343068/is-there-a-way-to-skip-password-typing-when-using-https-github>
- <https://marklodato.github.io/2013/10/25/github-two-factor-and-gnome-keyring.html>

## 概要

1. Git側の情報
    1. gitで認証情報を保存させるためには、credential helper を利用することができる
      - キャッシュすることもできる
    2. creadential storeとして利用できるものとして、以下などがある
      - Windows : git-credential-winstore, wincred
      - OSX : osxkeychain
      - Linux : gnome-keyring
2. SSHするときの情報
    1. SSH利用時は(たぶん、何も設定しない場合には)、DBUSの設定がないために、gnome-keyring-daemon に接続ができない
    2. 要は、DBUSの設定をすれば良い

## 試した設定方法
Debian sid (`uname -r # => 4.2.0-1-amd64`) を利用。

1. gnome-keyring, gnome-keyring-dev のインストール

    ```
    $ sudo apt-get install libgnome-keyring-dev
    ```
2. git credential のgnome-keyring用モジュールのビルド

    ```
    $ cd /usr/share/doc/git/contrib/credential/gnome-keyring
    $ sudo make
    ```
3. git config

    ```
    git config --global credential.helper /usr/share/doc/git/contrib/credential/gnome-keyring/git-credential-gnome-keyring
    ```
4. Xがない環境へのSSHを行う場合
    1. ログイン時に、gnome-keyringをstart
        以下を、/etc/pam.d/loginに追加する

        ```
        auth    optional        pam_gnome_keyring.so
        session optional        pam_gnome_keyring.so auto_start
        ```

    2. DBUSの開始
        以下を、.bashrc などに追加する

        ```
        if test -z "$DBUS_SESSION_BUS_ADDRESS" ; then
            eval `dbus-launch --sh-syntax`
        fi
        ```


### エラー内容
/var/log/audit.log に以下のような内容のエラーが出る

```
couldn't initialize prompt: GDBus.Error:org.freedesktop.DBus.Error.Spawn.ChildExited: Process org.gnome.keyring.SystemPrompter exited with status 1
```
