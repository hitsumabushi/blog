---
title: DebianでLuaJITTeXを使いたい
date: 2018-10-31T19:01:00+09:00
slug: '1901'
aliases:
  - 1901.html
categories:
  - blog
tags:
  - tex
  - debian
---



そろそろLuaTex使ってみたいなと思ったところ、LuaJITTeXの方が早い場合があるということで、試してみようと思った。

## 参考

* [luajittex のセットアップ](http://www.fugenji.org/~thomas/texlive-guide/luajitlatex.html)
    * そもそもこのサイトの情報が有用 [TeX Live を使おう──主に Linux ユーザのために──](http://www.fugenji.org/~thomas/texlive-guide/index.html)


## 未解決の問題

* `/var/lib/texmf/fmtutil.cnf-TEXLIVEDIST` が自動生成されている、とコメントされているが、元ファイルがわからない
```
### This file was automatically generated by update-fmtutil.
#
# Any local change will be overwritten. Please see the documentation
# of updmap on how to override things from here.
#
###
```

## 準備

パッケージインストール

```sh
sudo apt install texlive-lang-japanese texlive-latex-extra texlive-luatex
# 参考文献とか書くとき
sudo apt install texlive-bibtex-extra biber
```

`/var/lib/texmf/fmtutil.cnf-TEXLIVEDIST` を編集したい。(未解決の項目に書いた通り、元ファイルがわからないので直接編集している)

```diff
@@ -6,7 +6,7 @@
 ###
 dviluatex luatex language.def,language.dat.lua dviluatex.ini
 etex pdftex language.def -translate-file=cp227.tcx *etex.ini
-#! luajittex luajittex language.def,language.dat.lua luatex.ini
+luajittex luajittex language.def,language.dat.lua luatex.ini
 luatex luatex language.def,language.dat.lua luatex.ini
 mf mf-nowin - -translate-file=cp227.tcx mf.ini
 pdfetex pdftex language.def -translate-file=cp227.tcx *pdfetex.ini
@@ -14,7 +14,7 @@
 tex tex - tex.ini
 dvilualatex luatex language.dat,language.dat.lua dvilualatex.ini
 latex pdftex language.dat -translate-file=cp227.tcx *latex.ini
-#! luajitlatex luajittex language.dat,language.dat.lua lualatex.ini
+luajitlatex luajittex language.dat,language.dat.lua lualatex.ini
 lualatex luatex language.dat,language.dat.lua lualatex.ini
 mptopdf pdftex - -translate-file=cp227.tcx mptopdf.tex
 pdflatex pdftex language.dat -translate-file=cp227.tcx *pdflatex.ini
```

## 使い方

```sh
luajittex --fmt=luajitlatex.fmt {tex file}
```

問題なくコンパイルできれば、pdfが生成されるはず。

## VSCodeでTeXする

[LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) をインストールして、以下の設定をする。
参考文献が必要なときは、 `luajittex_with_bib` のレシピでビルドするように書いている。

```json
{
    "latex-workshop.chktex.enabled": true,
    "latex-workshop.latex.recipes": [
        {
            "name": "luajittex",
            "tools": ["luajitlatex"]
        },
        {
            "name": "luajittex_with_bib",
            "tools": [
                "luajitlatex",
                "biber",
                "luajitlatex",
                "luajitlatex"
            ]
        },
    ],
    "latex-workshop.latex.tools": [
        {
            "name": "luajitlatex",
            "command": "luajittex",
            "args": [
                "--cmdx",
                "--synctex=1",
                "--fmt=luajitlatex.fmt",
                "%DOCFILE%"
            ]
        },
        {
            "name": "biber",
            "command": "biber",
            "args": [
                "%DOCFILE%"
            ]
        }
    ],
    "latex-workshop.intellisense.surroundCommand.enabled": true,
    "latex-workshop.synctex.afterBuild.enabled": true,
}
```

## その他実際のTeXを書く時に参考になりそうなもののメモ

* 参考文献まわり
    * [BibTeXの書誌情報の書き方知りたいとき: Wikipedia](https://ja.wikipedia.org/wiki/BibTeX#.E6.9B.B8.E8.AA.8C.E6.83.85.E5.A0.B1.E3.83.95.E3.82.A1.E3.82.A4.E3.83.AB)
    * 参考文献を探したい時: Google Scholar