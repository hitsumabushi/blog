---
title: Debian でログインシェルをzshにしている人が snappy を使う場合の注意
date: 2018-04-11T10:58:00+09:00
slug: '1058'
aliases:
  - 1058.html
categories:
  - blog
tags:
  - debian
  - snappy
  - zsh
---


## Snappy について

* [Snappy](https://www.ubuntu.com/desktop/snappy)
* [snapcraft](https://snapcraft.io/)

Canonical が主導しているパッケージシステムで、Universal Linux Package と銘打つように、ポータブルなパッケージングができそうな感じ。
ポータビリティを上げるために、dockerみたいな感じで、依存ライブラリも全部パッケージに含めてしまうスタイルなので、多少debパッケージよりは大きくなる。
その分、sidを使っているとよく起きる、共通ライブラリの依存バージョンの不整合がおきる、という問題は起きない。

snapcraftのページではパッケージングの方法も紹介されているので、配布したい人自身がsnapパッケージを作りやすいはず。
少なくとも、ディストーションごとのパッケージを各アプリケーション作成者がやるよりは、遥かにやりやすい。
自動アップデートとかもあるので、サービス提供者が利用者に常に最新版を使ってもらいたい場合などにメリットもある。
実際、 Ubuntu以外にも、Debian, Arch Linux, Gentoo, Fedora, open SUSE などでも利用できる。

Snappy は、snapd というAPIデーモンが動くことになっている。

### snappy のインストール

```sh
$ sudo apt install snapd
```

### snap パッケージのインストール

```sh
$ sudo snap install hello-world
```

## 困ったこと

* Snappy でインストールしたアプリケーションへのパスが通らない
* Snappy でインストールしたデスクトップアプリケーションが、menuに登録されない

## 調べたこと

### バージョン

Kernel はpinningしているので、少し古い。

```sh
$ snap version
snap    2.32.3
snapd   2.32.3
series  16
debian
kernel  4.9.0-3-amd64
```

### snappy でインストールした場合のパス

* 実態はバージョンごとに、 `/snap/_app_name_/_version_/` 以下に置かれる。現在利用しているものへのリンクは `/snap/_app_name_/current/`
* コマンドは、 `/snap/bin/` 以下にコピーされる。
* デスクトップエントリのファイルは `/var/lib/snapd/desktop/applications/*.desktop` というファイルが作成される

### パスの設定方法について

`/etc/profile.d/apps-bin-path.sh` にパスを設定するためのスクリプトが置かれている。

```sh
$ cat /etc/profile.d/apps-bin-path.sh
#!/bin/sh --this-shebang-is-just-here-to-inform-shellcheck--

# Expand $PATH to include the directory where snappy applications go.
if [ "${PATH#*/snap/bin}" = "${PATH}" ]; then
    export PATH=$PATH:/snap/bin
fi

# desktop files (used by desktop environments within both X11 and Wayland) are
# looked for in XDG_DATA_DIRS; make sure it includes the relevant directory for
# snappy applications' desktop files.
if [ "${XDG_DATA_DIRS#*/snapd/desktop}" = "${XDG_DATA_DIRS}" ]; then
    export XDG_DATA_DIRS="${XDG_DATA_DIRS:-/usr/local/share:/usr/share}:/var/lib/snapd/desktop"
fi
```

zsh では `/etc/profile` などを読まないので、パスが設定できていない。
`/etc/zsh/zprofile` に、上記の内容を書いて置けば良い。
あるいは、 `/etc/zsh/zprofile` で以下のようにする。

```sh
for i in /etc/profile.d/*.sh ; do
    [ -r $i ] && source $i
done
```
