---
title: GolangでLinuxコマンドを書いた時のメモ
date: 2015-03-22T11:38:00+09:00
slug: '1138'
aliases:
  - 1138.html
categories:
  - blog
tags:
  - golang
draft: true
---


## やり始めて困ったこと
1. ディレクトリ構成をどうすべきか?
  loggerなど、共通のモジュールをどう配置するべきか迷った。

      ```
        - src
          |-- foo
          |   - foo.go
          |-- bar
          |   - bar.go
          L-- util : 共通モジュールはこのディレクトリ以下に
              - hogeee.go
      ```

2. packageの名前分割単位
  ディレクトリ構成から決める。foo以下なら、fooパッケージ。

3. コメントの書き方
  1. 関数のコメント : funcの上に書く
  2. package のコメント: packageの上に書く。(同じパッケージに複数書くと、多分ソートされて最初のやつ。)

## テスト
1. テストの仕方
  foo/foo\_test.goというファイルで書く。

      ```
      package foo

      import (
        "testing"
      )

      func TestSetLogger(t *testing.T) {
        if logging := SetLogger(); logging == nil {
        >-t.Errorf("Cannot Get Logger")
        }
      }
      ```

1. 型情報をどうやって取得するのか
  reflectパッケージを使う。

      ```
      reflect.TypeOf(0) // => reflect.Type オブジェクトが返る
      reflect.TypeOf(0).Kind()
      reflect.TypeOf(0).Name()
      reflect.TypeOf(0).NumMethod() // メソッドの数がわかる
      reflect.TypeOf(0).Method(0) // reflect.TypeOf(0)(=int)をレシーバとする0番目のメソッド
      ```

## 実装
1. 引数の扱い

  1. os.Argsを使う (全部自分でやるとき)
  2. flag パッケージを使う (ちょっと凝ったことをやるとき)

2. ファイルの情報を取得
    
  1. os.Stat
  2. io.Ioutil
  3. filepath.Walk


## 最低限やること
1. 引数を見て処理をする
2. 正規表現でやる
3. オプションの実装
4. 2, 3のオプションの実装


