Title: Intel NUC 上に vSphere 6.5 のVSAN環境を作る
Date: 2017-10-13 01:06
Category: blog
Tags: vmware

[TOC]

あまりVMwareを触らなくなってきて、何も見ずにvCenterの設定とかMaximum configurationsとか言えなくなってきたので、VMware周りのことをメモに残しておくことにする。
ひとまず、自宅のVSAN環境の構築メモ。

# 環境
以下の構成のIntel NUC 3台にESXiをインストールして、その上にvCenterを立て、VSAN環境を作る。
* Machine: NUC6i3SYH https://www.amazon.com/gp/product/B018NSAPIM
    * Memory: 16GBx2 https://www.amazon.com/gp/product/B015YPB8ME
    * Cache SSD: Intel 128GB https://www.amazon.co.jp/gp/product/B01JSJA1Z2
    * SSD: Crucial MX300 275GB https://www.amazon.com/gp/product/B01IAGSD5O
    * USB storage: SanDisk USB Flash Drive 8GB https://www.amazon.co.jp/gp/product/B005FYNSUA
        * ESXi インストール用
        * あんまり良くはないけど、省スペースのために妥協
    * USB NIC: StarTech.com USB32000SPT https://www.amazon.com/dp/B00D8XTOD0
        * 一時期、管理ネットワークとVSANネットワークを兼用していたが、すぐにぶっ壊れるので、NICを追加するために購入した
        * 4K までだけどJumbo frame がサポートされているので、まあ良さそう。もちろん本当は9K欲しい。
* NFS サーバー
    * vCenter をデプロイしたいだけなので、データストアがVSANと別に作成できれば何でも良い。
    * 外付けHDDとかでもたぶんできるし、vCenterを作成するESXi上ではない場所にデプロイできるならそれでも良い。
    * あと、vCenterデプロイ時にSingle host VSANを構成することができるようになっているみたいだけど、今回はライセンスの適用順とかの問題を考えたくなかったので、使わなかった

ESXi Customizer を利用する都合上、作業マシンはWindowsである必要がある(と思う)。

# 手順
ここでは、最初に StartechのUSB Ethernet adapterをインストール時点で使うために、ESXiのイメージカスタマイズから行う。
通常のESXiインストール後にvibでドライバを入れる場合には、 [このブログ](http://www.virtuallyghetto.com/2016/11/usb-3-0-ethernet-adapter-nic-driver-for-esxi-6-5.html) を参照すれば良い。

## ESXi用のバンドルファイルのダウンロード
[このブログ](http://www.virtuallyghetto.com/2016/11/usb-3-0-ethernet-adapter-nic-driver-for-esxi-6-5.html) のStep 0 にある、 `ESXi 6.5 USB Ethernet Adapter Driver Offline Bundle` をダウンロードする。
これを新しくディレクトリを作って(ここでは、 `C:\path\to\pkg` とする)保存しておく。

## ESXi イメージの準備
普通のESXi イメージを使っても良い。

[ESXi Customizer](https://www.v-front.de/p/esxi-customizer-ps.html) を使う。
事前に、 VMware PowerCLI をインストールしておく。
(VMware PowerCLI の最新版の場所はわかりづらい。たぶん https://www.vmware.com/support/developer/PowerCLI/ あたりに飛んで、新しそうなバージョンのリンクを踏めば良い。)

ESXi Customizer をインストールした場所で、以下のコマンドを実行する。
(`C:\path\to\pkg` は、先の手順で作成したディレクトリ)
```
.\ESXi-Customizer-PS-v2.5.1.ps1 -pkgDir C:\path\to\pkg -nsc
```

すると、 `ESXi-6.5.0-20171004001-standard-customized.iso` のような名前のISOファイルができる。

## オプション: USBでブートしてインストールできるようにする

今回は、CDに焼くのが面倒だったのでUSBからブートしてインストールする。
何かしらのUSBドライブを用意する。
[UNetbootin](http://unetbootin.github.io/) を利用して、用意したUSBドライブにイメージを書く。
見たままだけど、ディスクイメージの項目からISOファイルを選んで、USBドライブを選べび、OKを押せば良い。間違って変なドライブを選択しない限りは特に問題はない。

以下のインストールでは、このUSBドライブをIntel NUCに挿して行う。

## ESXi インストール

普通にインストールする。
boot時はF10連打してbootしたいドライブを選ぶ。
install先はインストール用のUSB(私の構成ではSanDiskのUSBドライブ)を選ぶ。

## インストール後の追加の初期設定

通常通り、管理ネットワークの設定やホスト名の設定を行う他に、NICを有効にする必要がある。
手順としては以下の通り。

* DCUI(もしくはSSH)に入れるようにして、DCUIに入る
* `esxcli software vib list` して、`vghetto-ax88179-esxi65` というvibが入っていることを確認する
* 以下を実行する
```
esxcli system module set -m=vmkusb -e=FALSE
```
* reboot
* 以下をDCUIで実行して、NICが見えていることを確認する
```
esxcli network nic list
```

自分の環境では以下のように見える。
```
[root@esxi-01:~] esxcli network nic list
Name    PCI Device    Driver        Admin Status  Link Status  Speed  Duplex  MAC Address         MTU  Description
------  ------------  ------------  ------------  -----------  -----  ------  -----------------  ----  --------------------------------------------
vmnic0  0000:00:1f.6  ne1000        Up            Up            1000  Full    b8:ae:ed:eb:0c:11  1500  Intel Corporation Ethernet Connection I219-V
vusb0   Pseudo        ax88179_178a  Up            Up            1000  Full    00:0a:cd:2f:23:6a  1500  Unknown Unknown
vusb1   Pseudo        ax88179_178a  Up            Down             0  Half    00:0a:cd:2f:23:6b  1500  Unknown Unknown
```

これを3台とも行う。

## NFS のマウント

vCenter をデプロイする先のデータストアが必要なので、どれか1台でNFSをマウントする。

## vCenter のデプロイ && VSANの設定

* vCenter は通常どおりデプロイする。CLIからデプロイした。
* VSANの設定も通常どおり行えば良い。
    * vDSを作って、VSAN用のportgroupを作る。今回の vusb0/1 はMTU4000までいけるので、必要に応じて、MTU4000にしておく
    * その後各ホストで、vmkアダプタを作って、VSAN用ポートグループにアサインして、VSANネットワークとして設定する
    * HAを有効化するのはVSAN有効化後に行う


# 参考
* ESXi Customizer: https://www.v-front.de/p/esxi-customizer-ps.html
* UNetbootin: http://unetbootin.github.io/
* virtuallyGhetto: http://www.virtuallyghetto.com/2016/11/usb-3-0-ethernet-adapter-nic-driver-for-esxi-6-5.html
