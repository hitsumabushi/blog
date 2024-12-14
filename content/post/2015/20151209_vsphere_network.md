---
title: vSphere環境でのQoS
date: 2015-12-09T10:05:00+09:00
slug: 1005
categories:
  - blog
tags:
  - VMware
  - vSphere
  - network
draft: true
---


# 資料
1. [vSphere 5.5 の新機能紹介 ネットワーク2 （トラフィックのフィルタリングとマーキング）](https://blogs.vmware.com/jp-cim/2013/09/vsphere-55-network02.html)
2. [QoS - DiffServ QoS Model](http://www.infraexpert.com/study/telephony7.html)

# VMware環境でのパケットのマーキング
vSphere 5.5以降、vDSを利用している場合、ポートグループ単位で、パケットのフィルタリングやマーキングができるようになった。
