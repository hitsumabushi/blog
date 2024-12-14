---
title: Rust を始めるための設定
date: 2017-02-07T23:55:00+09:00
slug: '2355'
categories:
  - blog
tags:
  - rust
  - vim
---


### rust のインストール

公式からインストールのためのスクリプトが提供されている。
これを使うと、rustup というrustのマネージャが使えるようになって、
rustc のバージョンアップや切替なんかができるらしい。

```
## rustup のインストール
curl https://sh.rustup.rs -sSf | sh

## これを .zshrc などに加える
source ${HOME}/.cargo/env
```

### rust のツールのインストール

cargo というので、いろんなライブラリとかツールをダウンロードできるらしい。
go get 的なノリだと思う。
ひとまず、補完とフォーマットのために以下の2つをインストールする。

```
## 割と時間がかかるので注意
cargo install rustfmt
cargo install racer
```

### vim の設定

[rust.vim](https://github.com/rust-lang/rust.vim), [vim-racer](https://github.com/racer-rust/vim-racer) の2つをインストールする。
設定は以下の通り。
```
" Rust
let g:rustfmt_autosave = 1
set hidden
let g:racer_cmd = "${HOME}/bin"
```

### hello world

例えば、以下のようなわざとフォーマットが崩れた状態のファイルを保存すると、保存時にフォーマットされる。
```rust
fn main() {println!("Hello,  world!");
}
```

最低限これで十分使えるけど、定義ジャンプとかもできたりするらしいので、その辺のショートカットの設定と、syntax エラーがわかるように設定をしたい。


### 参考

* [気付いたらRustの環境構築がかなり楽になってた](http://keens.github.io/blog/2016/12/29/kizuitararustnokankyoukouchikugakanarirakuninatteta/)
