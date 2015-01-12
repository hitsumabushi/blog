Title: vDSのポートバインドタイプ
Date: 2015-01-10 23:49
Category: blog
Tags: VMware, VCP, vDS

## 資料
[VMware KB: ESX/ESXi でのポート バインド タイプの選択](http://kb.vmware.com/selfservice/search.do?cmd=displayKC&docType=kc&docTypeID=DT_KB_1_1&externalId=2086886)

## ポートバインドタイプとは
vNICをvDSに接続するとき、ポートグループのポートがどのようにVMに割り当てられるかを、ポートバインドタイプとして、設定できます。
バインドのタイプは以下の3つから選択できました。(2つめの動的バインドは、ESXi5.0で廃止。)

1. 静的バインド (Static Binding)
2. 動的バインド (Dynamic Binding)
3. 短期バインド (Ephemeral Binding)

### 静的バインド
vNICが作成された段階で、直ちにポートにアサインされ、削除された時に初めて切断される。
vCenter Server経由の時に利用可能。

### 動的バインド
VMがパワーオンされていて、vNICが接続状態の時のみ、ポートにアサインされる。
パフォーマンスの観点から非推奨。

### 短期バインド
VMがパワーオンされていて、vNICが接続されている時に、ポートが作成され、アサインされる。
VMがパワーオフされるか、vNICが切断された時に、ポートが削除される。

短期バインドの場合のみ、vCenterがダウンしている際、VMのネットワーク接続を管理することができる。
256個までしか作れないとかパフォーマンスの問題から、リカバリ目的にのみ使用することが推奨。

## ポート数について
vSphere 5.1以降、静的ポートバインドの利用時、自動的にポートグループを拡張されるようになっている。
vSphere 5.0では無効だが、MOBのReconfigureDVPortgroup\_Taskを変更して有効にすることもできる。


