Title: vSphere環境でのQoS
Date: 2015-12-09 10:05
Category: blog
Tags: VMware, vSphere, network
Status: draft

[TOC]

# 資料
1. [vSphere 5.5 の新機能紹介 ネットワーク2 （トラフィックのフィルタリングとマーキング）](https://blogs.vmware.com/jp-cim/2013/09/vsphere-55-network02.html)
2. [QoS - DiffServ QoS Model](http://www.infraexpert.com/study/telephony7.html)

# VMware環境でのパケットのマーキング
vSphere 5.5以降、vDSを利用している場合、ポートグループ単位で、パケットのフィルタリングやマーキングができるようになった。
