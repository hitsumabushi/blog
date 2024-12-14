---
title: docker swarm init on Debian Sid
date: 2016-09-20T15:07:00+09:00
slug: '1507'
aliases:
  - 1507.html
categories:
  - blog
tags:
  - docker
  - debian
draft: true
---


## 内容
Debian Sid (2016/09/20 時点)で、 Docker Engine の swarm mode を初期設定したメモ。

## 手順

### docker engine の設定

[Installation on Debian](https://docs.docker.com/engine/installation/linux/debian/#/debian-wheezy-stable-7-x-64-bit)

```
sudo apt-get purge -y "lxc-docker*"
sudo apt-get purge -y "docker.io*"
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates
sudo apt-key adv --keyserver p80.pool.sks-keyservers.net --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo debian-stretch main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update -y
sudo apt-get install -y docker-engine
```

### swarm 初期化

```
# Manager
$ sudo docker swarm init --advertise-addr 192.168.253.158
Swarm initialized: current node (92c34zr76hdav65q97pybnii6) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-305k6qcpoghq89avwv0pu6dxj2e00utvno7hx7ctdp5no7meuu-737dwq5cmuab1p30hyx5rpd6t \
    192.168.253.158:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
$ sudo docker node ls
ID                           HOSTNAME    STATUS  AVAILABILITY  MANAGER STATUS
92c34zr76hdav65q97pybnii6 *  workdebian  Ready   Active        Leader
```

```
# Add worker nodes to manager
$ sudo docker swarm join --token SWMTKN-1-305k6qcpoghq89avwv0pu6dxj2e00utvno7hx7ctdp5no7meuu-737dwq5cmuab1p30hyx5rpd6t 192.168.253.158:2377
```

### swarm での動作

...

## TIPS

### systemd unit file の中で、 EnvironmetFile=- というのは一体なに?

[Custom Docker daemon options](https://docs.docker.com/engine/admin/systemd/) の例で、 `EnvironmetFile=-...` という形式の設定があった。これは一体なにか。
```
EnvironmentFile=-/etc/sysconfig/docker
EnvironmentFile=-/etc/sysconfig/docker-storage
EnvironmentFile=-/etc/sysconfig/docker-network
```

[systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)には書かれていない。
`EnvironmetFile` を含むいくつかの設定は、 [systemd.exec(5)](https://www.freedesktop.org/software/systemd/man/systemd.exec.html) というのに書かれている。(exec となっているが、 configurationについてのもの)

[EnvironmentFile=](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#EnvironmentFile=) によると、
```
    The argument passed should be an absolute filename or wildcard expression, optionally prefixed with "-", which indicates that if the file does not exist, it will not be read and no error or warning message is logged. This option may be specified more than once in which case all specified files are read. If the empty string is assigned to this option, the list of file to read is reset, all prior assignments have no effect.
```
と書かれている。

### どうして、ExecStart が2行書かれているの?

Dockerの unti fileを見ると、以下のように、`ExecStart=`が2つあり、1つは空、もう1つが実際に実行したいものを書いている、という設定を見ることになる。
```
ExecStart=
ExecStart=/usr/bin/dockerd ...
```

これは、こう書かないといけない、という類のものらしい。
1つ目は設定を消すためのもので消していないと、複数回ExecStartが書かれているという内容のエラーが出る。

* [参考情報](https://github.com/docker/docker/issues/14491)

### tar.gz をダウンロードして、どこかのディレクトリに展開する

下記のように、curl でダウンロードしたものを標準出力に出して、それを tar で受けるのが、docker iamgeを小さく保つのには良さそう
```
RUN curl -sL "https://github.com/.../archive/${VERSION}.tar.gz" | tar -xzC "${APACHE_WEBROOT_DIR}" --strip-components=1
```

tar のオプションとして、 `-C` でディレクトリを指定していて、 これだけだと、ディレクトリの下に、解凍時に(割と一般的に)作成されるトップのフォルダができてしまうので、
`--strip-components=1` にして、トップのフォルダを無視する。

ちなみに、デバッグしたくなったら、以下のように `od` をすると便利そう。
```
RUN curl -sL "https://github.com/.../archive/${VERSION}.tar.gz" > /tmp/x && od -c /tmp/x | head
```

