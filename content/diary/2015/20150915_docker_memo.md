Title: Dockerの細々としたメモ
Date: 2015-09-15 04:21
Category: blog
Tags: docker, debian

Debian で利用する際のメモを書いておく。

[TOC]

## grub でのカーネルパラメータ

1. systemd を利用する設定
2. cgroups で、メモリに制限をかけるための設定

```sh
# quiet はあってもなくても良い
GRUB_CMDLINE_LINUX_DEFAULT="quiet init=/bin/systemd"
GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
```


## cgroups まわり

cgroups のディレクトリ配下に設定がある

```sh
/sys/fs/cgroup/cpu,cpuacct/docker/
```

## network

[参考: Dockerのネットワーク管理とnetnsの関係](http://enakai00.hatenablog.com/entries/2014/04/24)

docker コンテナを1つ立ち上げるごとに、vethデバイスができる

```sh
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:0c:29:e1:2c:42 brd ff:ff:ff:ff:ff:ff
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 00:0c:29:e1:2c:4c brd ff:ff:ff:ff:ff:ff
4: docker0@NONE: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether ba:fe:c4:10:27:19 brd ff:ff:ff:ff:ff:ff
8: veth279cc5b@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master docker0 state UP mode DEFAULT group default qlen 1000
    link/ether ba:fe:c4:10:27:19 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```

### netns : network namespace

```sh
$ ls -l /proc/{{.State.Pid}}/ns/
合計 0
lrwxrwxrwx 1 root root 0  9月 15 04:38 ipc -> ipc:[4026532695]
lrwxrwxrwx 1 root root 0  9月 15 04:38 mnt -> mnt:[4026532693]
lrwxrwxrwx 1 root root 0  9月 15 04:38 net -> net:[4026532599]
lrwxrwxrwx 1 root root 0  9月 15 04:38 pid -> pid:[4026532696]
lrwxrwxrwx 1 root root 0  9月 15 04:38 user -> user:[4026531837]
lrwxrwxrwx 1 root root 0  9月 15 04:38 uts -> uts:[4026532694]
```

### iptables

```sh
$ sudo iptables-save | grep -v "^#"
*nat
:PREROUTING ACCEPT [28:2281]
:INPUT ACCEPT [27:2197]
:OUTPUT ACCEPT [68:6733]
:POSTROUTING ACCEPT [68:6733]
:DOCKER - [0:0]
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
COMMIT
*filter
:INPUT ACCEPT [16482:42893307]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [12048:507911]
:DOCKER - [0:0]
-A FORWARD -o docker0 -j DOCKER
-A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i docker0 ! -o docker0 -j ACCEPT
-A FORWARD -i docker0 -o docker0 -j ACCEPT
COMMIT
```

#### 設定の意味

## storage

- [RHEL7におけるDockerのディスクイメージ管理方式](http://enakai00.hatenablog.com/entry/20140420/1397981156)
- [Resizing Docker containers with the Device Mapper plugin](http://jpetazzo.github.io/2014/01/29/docker-device-mapper-resize/)


