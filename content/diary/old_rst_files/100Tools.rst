便利なツール
################

:date: 2014/01/02 02:40:20
:tags: perl
:category: blog

POD
----
* Plain Old Documentation
* man perldoc を参照

lwp-request
------------
* Webサーバーにリクエストを送って、適当な形式に変換してくれる
* GET, POST, PUT も選べる。
* 出力形式としては、 text, ps, links, html, dump

.. code-block:: perl

   lwp-request -o text www.example.com


Text::Autoformat
------------------

Text::Tabs
------------
* タブをスペースに変換

String::Approx
-----------------
* あいまいなマッチをする


Template-Toolkit
-----------------

Lingua::En::Inflect 'PL_N'
---------------------------
* 単数形と複数形を変換してくれる
