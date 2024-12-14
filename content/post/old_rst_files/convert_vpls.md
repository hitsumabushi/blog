---
title: VPLSについてのメモ
date: 2014-01-06T02:43:20+09:00
slug: 0245
tags:
  - vpls
categories:
  - blog
---

## What is VPLS

-   Virtual Private LAN

-   MACフレームを、ルーターを含むネットワークを超えて、やり取りするための技術の1つ

-   

    MPLSはIPにラベルをつけるが、VPLSはMACにラベルをつけるというイメージ

    :   -   ラベルを使う理由としては、元々、経路計算を高速にしたかったはずだけど、今はそんなに気にしなくて良いっぽい

## Why VPLS

MPLSが便利なのと、同じ。

-   VPN

-   

    TE(Trafic Engineering)

    :   -   明示的な経路選択
        -   回線使用率から選択したり。
        -   ループフリー&自由なネットワークトポロジー

-   

    障害検知&切り替え

    :   -   FRR(Fast ReRoute)
        -   代替経路へ即座に切り替えが起こる
        -   1 sec以内で切り替えられるらしい

## 参考サイト

0.  RFC 4761, 4762
1.  <http://itpro.nikkeibp.co.jp/article/COLUMN/20070130/259589/>
2.  <http://www.itbook.info/study/mpls2.html>

MPLSについては以下が参考になる

1.  <http://www.atmarkit.co.jp/fnetwork/tokusyuu/11mpls/mpls01.html>
