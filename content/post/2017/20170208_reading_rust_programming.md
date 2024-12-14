---
title: Rust の学習メモ
date: 2017-02-08T00:42:00+09:00
slug: '0042'
categories:
  - blog
tags:
  - rust
draft: true
---


## 資料

* https://doc.rust-lang.org/book/
    * 日本語訳(バージョンが違うかも) : https://rust-lang-ja.github.io/the-rust-programming-language-ja/1.6/book/

## getting started

* `println` と `println!` は違う
    * `!` があるとマクロ呼び出し
* Rust の特徴
    * Rustは `expression-oriented` で 末尾に `;` が入る
    * 式なので、返値を持つということだと思う
* コンパイル
    * rustc でコンパイルすると、 実行ファイルはデフォルトでは、 xxx.rs なら xxx になるっぽい
* Cargo
    * コードのビルド、ライブラリのダウンロード、ライブラリのビルドが管理できる
    * ディレクトリ構成の制約がつく。
        * 直下に `Cargo.toml` や README.md, LICENCEなどのファイル
        * `src/` 以下にソースコード
    * Cargo.toml : プロジェクト設定ファイル
        * `packages` に name, version, authors などを記載
    * `cargo build` すると、 `target/debug/_name_` としてバイナリが作成される
        * 直接実行しても良いが、 `cargo run` すれば良い
        * リリースビルドのためには、 `cargo build --release`
    * リリースビルドは、実行速度は速くなるが、コンパイル時間が長くなる
        * さらに、 `Cargo.lock` ファイルが作成される
        * 依存関係の追跡をするために必要
* Cargo を使って、新しいプロジェクトを作成することもできる
    * 実行ファイルを作成したい場合、 `cargo new _name_ --bin`
    * ライブラリの場合には、 `cargo new _name_`

## Syntax and Semantics

* "1つの値に対して、複数の名前が対応することはない" っぽいことが書いてあったけど良くわかっていない
    * http://qiita.com/cactaceae/items/2c70a9947364c60ec100 この辺を読めば例が書かれていそう
* 型アノテーション を最低限入れておけば型推論してくれる
    * 整数型として可能なサイズは、8, 16, 32, 64bitで、最初に iがついていれば符号付き、そうでない場合には u をつける。
* 束縛はデフォルトで immutable
    * もし mutable にしたいのであれば、 `let mut x=5; x=10;` など、`mut` をつける
    * `let x=100; let x=10;` みたいなのは書けるけど、どう考えれば良い?
        * shadowing というらしい。全然違う型でも被せられる
        * 良いことなのか...?
* 変数を初期化せずに宣言できるが、それを初期化しないまま使うことは許されていない
* 文字列フォーマット: [https://doc.rust-lang.org/std/fmt/](https://doc.rust-lang.org/std/fmt/)
* `ブロック` というもの ( `{` と `}` で囲まれた範囲 ) があって、 変数のスコープになる
