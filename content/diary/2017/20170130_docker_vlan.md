Title: docker: メモ
Date: 2017-01-30 18:12
Category: blog
Tags: docker
Status: draft

[TOC]

## Docker 検証
### vmx
* 踏み台: nic 3本で検証
    * SSH用
    * VLAN=279
    * VLAN trunk

### VLAN設定
#### 資料
https://wiki.archlinuxjp.org/index.php/VLAN

#### やったこと
SSHでログインして以下を実行
```sh
## module 
sudo lsmod | grep 8021q
sudo modprobe --first-time 8021q
sudo lsmod | grep 8021q

## valn device
sudo ip link add link eth2 name eth2.279 type vlan id 279
sudo ip addr add 192.168.16.32/24 dev eth2.279
ip a show eth2.279
## 6: eth0.279@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
##     link/ether 00:50:56:ba:1c:cd brd ff:ff:ff:ff:ff:ff
##     inet 192.168.16.32/24 scope global eth0.279
##        valid_lft forever preferred_lft forever
sudo ip link set dev eth2 up
sudo ip link set dev eth2.279 up
```

片方のインターフェースからのpingが返ってこない...
* http://d.hatena.ne.jp/hirose31/20120822/1345626743
* http://e-garakuta.net/techinfo/doku.php/linux/advanced-routing

```sh
ip rule show
## 0:      from all lookup local
## 32766:  from all lookup main
## 32767:  from all lookup default
sudo ip rule add from 192.168.16.31 table 200 prio 200
sudo ip route add default dev eth1 src 192.168.16.31 table 200
sudo ip rule add from 192.168.16.32 table 300 prio 300
sudo ip route add default dev eth2.279 src 192.168.16.32 table 300
```

