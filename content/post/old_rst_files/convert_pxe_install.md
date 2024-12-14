---
title: PXEブートでインストーラを起動する
date: 2014-01-01T02:44:20+09:00
slug: '0244'
tags:
  - pxe
  - preseed
  - kickstart
categories:
  - blog
---

最近、VMwareのESXiで仮想環境を作っています。
触っていて気づいたのですが、空の仮想マシンを起動するとPXEブートを試みてくれます。
この仕様をうまく使いたいなーと思って、PXEブートでインストールを自動化する方法を調べました。

PXEブートしてインストールを自動化するまでの手順を簡単に書いていきます。
Debianをインストールサーバーとして予め立てておき、DebianまたはCentOSをインストールすることにします。


## 1. Debian Install

最初のDebianはCDやらで手動でインストールしてください。
Debianのインストール手順は省略します。

## 2. DHCPサーバーを立てる

``` sh
# Install DHCP Server
apt-get install isc-dhcp-server

# Config DHCP : INTERFACES
vi /etc/default/isc-dhcp-server
# Modify INTERFACES="" to INTERFACES "eth1"

# Config DHCP : Server setting
vi /etc/dhcp/dhcpd.conf
```

編集する箇所は以下の通りです。

<https://gist.github.com/10664868>

DHCPサーバーを再起動して設定を反映させます。

``` sh
# Restart DHCP Server
/etc/init.d/isc-dhcp-server restart
```

## 3. TFTPサーバーを立てる

デフォルトで大丈夫でした。

``` sh
# Install TFTP Server
apt-get install tftpd-hpa
```

## 4. PXEブート用のイメージを準備する

以下のページから適当にnetbootイメージを選んで、netboot/netboot.tar.gzを取って来ます。

-   <http://www.debian.org/distrib/netinst#netboot>

``` sh
# 展開する
tar xvf netboot.tar.gz
# move files to root dir of TFTP
mv ./* /srv/tftp
```

## 5. 中間チェック

この段階でPXEブートしてみると、Debianのインストーラが立ち上がるようになります。

### ブート画面でOSを選択できるようにする

## 6. CentOSのインストーラを準備

1.  mkdir -p /srv/tftp/centos/6.5/x86_64

2.  CentOSのインストールDVDを持って来る

3.  mount -o loop \<CentOS install ISO\> /media

4.  

    /media/images/pxeboot/にある次の2つのファイルを/srv/tftp/centos/6.5/x86_64/以下にコピーしてくる

    :   -   initrd.img
        -   vmlinuz

5.  umount /media

ここで、Debianのインストーラたちも整理して、 /srv/tftp/debian/7.4/amd64
以下にあるとします。:

    /srv/tftp/
        |
        |-debian/7.4/amd64/
        |   |
        |   |-boot-screens
        |   |
        |   |-initrd.gz
        |   |
        |   |-linux
        |   |
        |   |-pxelinux.0
        |   |
        |   |-pxelinux.cfg/default
        |
        |-centos/6.5/x86_64
        |   |
        |   |-initrd.img
        |   |
        |   |-vmlinuz
        |
        |-pxelinux.0 -(シンボリックリンク)-> debian/7.4/amd64/pxelinux.0
        |
        |-pxelinux.cfg -(シンボリックリンク)-> debian/7.4/amd64/pxelinux.cfg

## 7. メニューの作成

pxelinux.cfg/defaultの内容を以下のように編集します。
後でもう少し修正します。
[最終形はGistにあがっているので](https://gist.github.com/10663699)、
そちらを見てください。

``` sh
# D-I config version 2.0
default debian/7.4/amd64/boot-screens/vesamenu.c32

# Boot Menuに入りたい
prompt 1
timeout 300
menu title - Boop Options Menu -

label Debian-7.4
    menu label ^0 Debian 7.4
    #include debian/7.4/amd64/boot-screens/menu.cfg
    kernel debian/7.4/amd64/linux
    append priority=critical vga=788 initrd=debian/7.4/amd64/initrd.gz

label CentOS-6.5
    menu label ^1 CentOS 6.5
    kernel centos/6.5/x86_64/vmlinuz
    append initrd=centos/6.5/x86_64/initrd.img
```

### Debianインストールの自動化

| ここまでで、PXEブートさえしていれば、複数のOSを選んでインストールできるようになりました。
| いまのところの問題点としては、結局インストーラを起動した後は手作業になっていることです。
| 次は、PXEブートした後、放っておくと勝手にインストールが終わっているようにしましょう。

| Debianの場合にこれを実現するには、preseedと呼ばれる設定ファイルを書けば良いです。
| 普通にインストールするときに色々な質問に答える必要があると思いますが、その答えを事前に書いておくものです。
| ただ、preseedが読まれる前に、インストーラから質問される(インストールのタイプなど)ことがあるので、そのあたりはブート時のパラメータとして渡しましょう。

## 8. preseed ファイル作成

| preseedファイルはかなり長いです。
| 昔はpreseedのドキュメントを読んでも、作るの大変だった印象があったのですが、[コメント付きのpreseedの例がある](https://www.debian.org/releases/wheezy/example-preseed.txt)
  ので、これを元に書いて行けば特に大きくは困らないです。
| ただ、例に書かれていないのですが、GRUBの設定を追加しないといけないのはわかりづらいかも知れません。
| preseedで細かく設定しようとすると大変なので、それはAnsibleなどインストール終わってからの自動化に入れる方針です。

| 今回はパーティションなどは全部インストーラに任せています。
| パーティションを変える場合などは、コメントアウトされているところを変更してください。

<https://gist.github.com/10664868> の preseed.cfgを参照。

## 9. pxelinux.cfg/default 書き換え

| 今書いたpreseedファイルを debian/7.4/preseed.cfg
  として配置したことにします。
| ブートオプションなどを追加した pxelinux.cfg/default
  ファイルは以下のようになります。

| あとでどうせCentOSも自動化するので、そちらもあわせてオプションをつけておきます。

<https://gist.github.com/10664868> の defaultを参照。

## 10. Debianインストールのチェック

| また実際にPXEブートしてみましょう。
| Debianをメニューで選択すると、今度は勝手に画面が進んで行くと思います。
| 最後までインストールが終わり、勝手にリブートされてこれば、成功です。s

### Cent OSインストールの自動化

## 11. httpサーバー作成

| 後でやるように、kickstartファイルはhttp経由で配ろうと思います。(TFTPでできないっぽかった)
| なので、httpサーバーを予め立てておくことにします。

``` sh
# apache install
apt-get install apache2
```

## 12. CentOSイメージのマウント

``` sh
mkdir -p /var/www/images/centos
mount -o loop <CentOS install ISO> /var/www/images/centos
```

## 13. kickstartファイルの準備

kickstartファイルの詳細については、
[redhatのページ](https://access.redhat.com/site/documentation/ja-JP/Red_Hat_Enterprise_Linux/6/html/Installation_Guide/s1-kickstart2-options.html)
が参考になります。というか、コレ見たら大体で書ける。

今回使っているkickstartfileは以下の通りです。

<https://gist.github.com/10664868> の kickstart.cfgを参照。

## 14. kickstartファイルの配置

| pxelinux.cfg/defaultファイルの内容に合わせて、kickstart.cfgを配置します。
| 今回は、apacheのドキュメントルート直下に置けば良いようにしました。

``` sh
mv kickstart.cfg /var/www/
```

## 15. CentOSインストールのチェック

| 最後に、CentOSのインストールを確かめます。
| 実際にPXEブートして、CentOSをメニューで選択すると、勝手に画面が進んで行くと思います。
| 最後までインストールが終わり、勝手にリブートされてこれば、成功です。

### もっと自動化できるけど\...

| 今回は、インストールの自動化を行いました。
| 一応、インストールするOSの種類を選ぶところを手でやることにしましたが、普通はOSは一種類で良いか、MACアドレスでインストールするOSを分けてしまうのだと思います。
| そうしておけば、OSの種類を選ぶところも自動化することができます。
| 自分としては、基本はDebianをインストールしたくて、たまにCentOSも選びたいという程度なので、ここまでで止めておきます。

| 機会があれば、preseedやkickstartでホスト依存な部分(例えば固定IPとか)を都度生成してインストールする方法も考えたいですね。

### さらに読もうと思ってるサイト

-   

    <http://d.hatena.ne.jp/fujisan3776/20100630/1277861431>

    :   インストール中は別の作業をしているので、インストールが終わったことも知らせて欲しい
