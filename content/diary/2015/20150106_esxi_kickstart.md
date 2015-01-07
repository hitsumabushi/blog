Title: ESXiをkickstartでインストールする
Date: 2015-01-06 23:38
Category: blog
Tags: VMware, ESXi

ESXiをPXEブートして自動インストールする方法について、日本語での説明があまりなかったので、メモとして残しておく。

## 利用OS
- ESXi 5.5
- Debian 7.7 (DHCPサーバー, HTTPサーバーを兼務させる)

## DHCP, TFTP, HTTPサーバーの準備
### 必要なソフトウェアのインストール

```sh
apt-get install tftpd-hpa isc-dhcp-server xinetd apache2
```

### DHCPサーバーの設定
BOOTPでインストールするため、あまり自由度がない。

[gist:id=b4e9a0e8e0ef68af1d6f,file=dhcpd.conf]

### TFTPサーバーの設定

適当なディレクトリ以下を公開する。
ここでは、/srv/tftp とする。

### kickstartイメージの準備

まずESXiのイメージの内容をもらってくる

```sh
cd /srv/tftp/
mkdir esxi
mount -o loop <ESXiのISO>.iso
rsync -a /mnt/esxi/
```

次に、pxe boot用のイメージを準備する。
必要なのは、pxelinux.o, pxelinux.cfg/

```sh
wget http://ftp.nl.debian.org/debian/dists/wheezy/main/installer-amd64/current/images/netboot/netboot.tar.gz
tar xvf netboot.tar.gz
```

### PXEブートの設定ファイル
* pxelinux.cfg/default

[gist:id=b4e9a0e8e0ef68af1d6f,file=default in pxelinux.cfg]

* esxi/boot.cfg
        * もともとあるファイルの / を除去していく
        * prefixを代わりに設定

[gist:id=b4e9a0e8e0ef68af1d6f,file=boot.cfg]

### kickstart file

以下のファイルを /var/www/servers/ks.cfg として保存。
(ここでは、httpでやっているが、tftpでやっても良い。)

[gist:id=b4e9a0e8e0ef68af1d6f,file=ks.cfg]

以上で、キックスタートの準備が終わる。

## 考えること
- サーバーごとの個別設定の渡し方
  事前にMACアドレスがわかっている場合にはできるけど、そうでない場合には、難しい。

