---
title: Perl のコンパイラオプション
date: 2014-01-01T02:37:20+09:00
slug: '0237'
aliases:
  - 0237.html
tags:
  - perl
categories:
  - blog
---


## 参考ページ

-   man perlrun
-   [DebugIto\'s - Perl/コマンドライン](http://debugitos.main.jp/index.php?Perl%2F%A5%B3%A5%DE%A5%F3%A5%C9%A5%E9%A5%A4%A5%F3)

## 基本的なオプション

### -e

-   ワンライナーを書くために必須。
-   複数並べられるので、それなりに色々書ける
-   直後にperlプログラムを書ける。

``` perl
perl -e 'print 11/2'
```

### -l\[8進数\]

-   行末に指定された8進数に変える。-l のみの場合、改行になる。

``` perl
perl -e 'print 22'       #=> 22
perl -l -e 'print 22'    #=> 22\n
perl -l101 -e 'print 22' #=> 22A
```

### -0\[digits\]

-   -l の入力セパレータバージョン

-   -00 とすれば、空行を区切り。段落モード。

    > -   \$/ = \"\";

-   -777 とすればファイルごとの区切りになる。

## 使い勝手の良いオプション

### -n

-   while (\<\>) { \...} の中にスクリプトを入れたと思って実行

### -p

-   -n みたいなもの。ただし、行(\$\_)を出力する。
-   sed に似たやつ。

### -a

-   -n, -p と一緒に使用
-   \$\_ を自動的に改行で分割し、配列 \@F に入れる

``` perl
perl -ane 'print $F[0], "\n"' /etc/passwd
```

### -F/pattern/

-   -a の分割のデリミタを指定する
-   パターンは複数文字でも良い。そのときは、\' \' または / / で囲む

``` perl
perl -F':' -ane 'print $F[0],":",$F[2] ,"\n"' /etc/passwd
```

### -i\[拡張子\]

-   拡張子がないとき、\<\>のファイルを直接編集する
-   拡張子があるとき、\<\>の元ファイルは、拡張子をつけたファイルにバックアップされる。
-   \$SECONDS を使うのがオススメ

``` perl
perl -i.back -pe `s/foo/bar/g' sample.txt
perl -i.$SECONDS -pe `s/foo/bar/g' sample.txt
```

## デバッグに使えるオプション

### -c

-   スクリプトのシンタックスチェックのみ行う

### -d\[:debugger\]

-   debugger の下で走らせる

### -w

-   より多くの Warning を出す

### -W (-X)

-   すべての Warning を出す(出さない)
