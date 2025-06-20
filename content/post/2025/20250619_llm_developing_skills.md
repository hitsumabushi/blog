---
title: LLM時代のソフトウェア開発に必要な新しいスキルセットについて悩んでいる
date: 2025-06-14T22:00:00+09:00
slug: '0200'
aliases:
  - 0200.html
categories:
  - blog
tags:
  - LLM
---


## 書き出し

AIやらLLMがソフトウェアデリバリのサイクルにどんどん入ってきて、エンジニアに求められるスキルセットが大きく変化していくと思っている。
本当に高度な専門性がない領域の単純なコーディング作業はLLMが担い、人間はより高度な判断と検証に注力する時代になっていくのは間違いないのかなというのが現状の所感。

そういうのもあって、じゃあ実際コーディング作業を全部LLMに任せたとしたら、どんなスキルが必要なんだろう、というのを、それなりにコードを書いたり計測したりが必要なPoCで試した感想を整理したい。

## 試していたこと

PoCのテーマとしては、Bloom filterでキャッシュorストレージアクセスの必要性を判断して、アクセスを減らすことで、どれだけレイテンシーやキャッシュヒット率が改善するのか、というもの。

GolangでAPIサーバーを実装し、ストレージとしてはredis、bloom filterはlocalメモリ上にした。
基本的なAPI request/responseの定義だけしか考えておらず、実装しようと思うとそれなりに面倒だな、という印象の作業になる。
しかも実装はそれなりにシンプルでも計測側が面倒なことが多い。キャッシュヒット率などを色々コントロールしてテストシナリオを調整して、bloom filterの効果を計測したり、ストレージまでのlatencyごとに、キャッシュヒット率 vs API全体のlatencyの変化を計測したり、とやることがそれなりにあった。

LLMでこれを(仕事が終わったあとにやって)2日で実装・計測できた。
ただ、これをやっていると、今後数年で自分のエンジニアとしての価値をどう出していくか難しいなと思う。(自分がアイデアとしてはずっと持っていたのに、面倒で放置していた)PoCをこれだけ高速に、おそらく誰でも実装できる状況になっているということで、スキルの伸ばし方も変えていく必要がある。


## 今後LLMと開発するうえで必要になりそうなスキル

まず今日時点で、LLMは全く万能ではない。
非常に細かいコードのスコープでは合っていても、システムアーキテクチャ観点ではそうしなくない?みたいなレベルのことをやる。あと、こうするとセキュリティだったり運用的に面倒だからしないでしょ、みたいな常識がない。

なので、うまく全体を見たり、誘導しないといけないケースがある。

LLMとの開発が本格化してくると、アーキテクチャの提案、コードの生成、バグ修正の提案、ドキュメント作成など様々なタスクをLLMでやるようになると思われる。
このとき、人間なら、せいぜいチームサイズのメンバーのレビューをしっかりするくらいで良いが、LLMといっしょに仕事をすると並列に出してくるし、速度も人間の比ではない。
1人あたりのコードベースで30倍とかを管理するようになっていくのではないだろうか?

そうなったとき、現状の数倍の速度で作成されるPRに対して、LLMの出力の正当性を要点を把握して大雑把に修正していく能力が求められると思われる。もちろんレビューにもLLMが付き合ってくれるが、何を担保することが大事なのだろうか?
自分がボトルネックにならずにPRを大雑把に確認し、リリース前に問題に気づくための方法論を確立していくことが必要に思われる。システム特性やSLIなどによって変わっていくものだと思われるが、ガードレールをどこにどう置くかをデザインしていくのが大切に思う。

## やらないとやばいなと思ったこと

逆に、自分に全く強みがない分野(自分はフロントエンドはあまり書かない)だと、もうLLMの言うことを受け入れて、困ったら修正すれば良いや、となりがちだった。大局観や要点についての勘所がなく、大量のコードベースを前にして、レビューをしていくことが難しかった。
これ自体は良いのだが、おそらくこれまでの開発フローだと、わからなくてもある程度は読み解いていくし、少しずつ調べて理解し、身につけていくというプロセスがあったと思う。だけども、より大量にコードが生成されていくと、なかなかそういった時間が取りづらくなっていくのではないか。
そうなると、どうやってLv.1の能力をLv.2, 3と上げていくのか、方法論もそうだが、漫然とやると見た目錠できてしまうので、モチベーション的にも難しくなっているなと感じる。

## なんとなくLLMが苦手なのかなと思ったところ

苦手というか、プロンプトで与えるのも結構骨が折れるし、人間が理解してレビューした方が良いかなと思った点

- システム設計の決定
- ビジネスロジックをシステムロジックに落とし込むときの理解
- パフォーマンスチューニング: レイヤがまたがると途端にアドバイスが必要になる


## まとめ

まとめになっているのかわからないが、LLM時代のエンジニアには、以下の能力が必要なのかなと思っている。

1. 問題を適切に分解し、LLMに伝える能力
2. 出力を素早く検証し、要所を抑えて問題を発見する能力
3. 大規模なシステム・要件を分割して、LLMで扱いやすいサイズの単位に設計する能力
4. LLMと人間の役割を適切に分担する判断力

LLMの能力に応じて、それぞれの要素に求められることも変わると思うが、ビジネス側の要求として、1人のエンジニアが扱う領域は、広くなるか、深くなるかだろう。
クラウドが普及して、それぞれのエンジニアロールに求められるスキルセットが変わっていったように、LLMでも変わっていくことが予想されるが、短期的に見ても、物量という観点で大きな変化がある。
物量を処理するためにも、高いエンジニアリングレベルの領域をしっかりと深めていく必要があるので、まずはLLMに振り回されすぎずにスキルを高めておくのがキャッチアップとしては良いかな。

