Title: 自宅 vSphere 上の CoreOS (Container Linux) のデプロイメモ
Date: 2017-02-08 22:31
Category: blog
Tags: coreos, containerlinux

[TOC]

## 構成

Mesos などを立てるため、Master 3台, Slave 2台以上の予定で作る。

## OSイメージ
VMware用のイメージを利用。
`/usr/share/oem/cloud-config.yml` に vmware tools周りの設定が入っているので便利。

## password の変更

grub で linux...の行の末尾に coreos.autologin と入れてパスワードなしログインをしてから、パスワード変更する。

## 初期設定: cloud-config

`/var/lib/coreos-install/user_data` を編集する。
(作法を無視すれば、 `/usr/share/oem/cloud-config.yml` でも良いはず。)

```
#cloud-config
coreos:
  units:
    - name: docker-tcp.socket
      command: start
      enable: true
      content: |
        [Unit]
        Description=Docker Socket for the API

        [Socket]
        ListenStream=2375
        BindIPv6Only=both
        Service=docker.service

        [Install]
        WantedBy=sockets.target

    - name: ens192-static.network
      runtime: false
      content: |
        [Match]
        Name=ens192

        [Network]
        Address=192.168.101.11/24
        Gateway=192.168.101.1
        DNS=8.8.8.8
        DNS=8.8.4.4
    - name: down-ens192.service
      command: start
      content: |
        [Service]
        Type=oneshot
        ExecStart=/usr/bin/ip link set ens192 down
        ExecStart=/usr/bin/ip addr flush dev ens192
    - name: ens224-static.network
      runtime: false
      content: |
        [Match]
        Name=ens224

        [Network]
        Address=192.168.105.11/24
    - name: down-ens224.service
      command: start
      content: |
        [Service]
        Type=oneshot
        ExecStart=/usr/bin/ip link set ens224 down
        ExecStart=/usr/bin/ip addr flush dev ens224
    - name: systemd-networkd.service
      command: restart

ssh_authorized_keys:
  - "ssh-rsa ..."
hostname: "coreos-00x"
users:
  - name: "hitsumabushi"
    passwd: "hashed password: https://coreos.com/os/docs/latest/cloud-config.html#users"
    groups:
      - "sudo"
      - "docker"
    ssh-authorized-keys:
      - "ssh-key ..."
write_files:
  - path: "/etc/resolv.conf"
    permissions: "0644"
    owner: "root"
    content: |
      nameserver 8.8.8.8
      nameserver 8.8.4.4
```

## もうすこし設定する

### NTP
デフォルトで、 systemd-timesyncd が上がっていて、 /etc/ntp.conf をみると `[0-3].coreos.pool.ntp.org` へ接続している。

### etcd2

```
coreos:
  etcd2:
    # generate a new token for each unique cluster from https://discovery.etcd.io/new?size=3
    discovery: "https://discovery.etcd.io/<token>"
    # multi-region and multi-cloud deployments need to use $public_ipv4
    advertise-client-urls: "http://192.168.101.11:2379"
    initial-advertise-peer-urls: "http://192.168.105.11:2380"
    # listen on both the official ports and the legacy ports
    # legacy ports can be omitted if your application doesn't depend on them
    listen-client-urls: "http://0.0.0.0:2379,http://0.0.0.0:4001"
    listen-peer-urls: "http://192.168.105.11:2380,http://192.168.105.11:7001"
...
  units:
...
    - name: etcd2.service
      command: start
...
```

### locksmith
```
coreos:
  update:
    reboot-strategy: "best-effort"
...
  units:
...
    - name: locksmithd.service
      command: start
```

