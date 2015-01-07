Title: VMware 環境でのMACアドレス割当て
Date: 2014-12-17 14:40
Category: blog
Tags: VMware, VCP

[TOC]

## 1. まとめ
vSphere環境上のMACアドレス割当の方式は、複数あります。自分のOUIを割当てたい!!、という場合には、

1. vCenter環境でプレフィックス指定
2. 固定割当て

といった方法を使いましょう

## 2. MACアドレスの割当て方式

1. vCenterによる自動割当て
    1. VMware OUI
    2. プレフィックスベース
    3. 範囲ベース
2. vCenterに接続されていないESXiによる自動割当て
3. 手動での割当て

### vCenterによる自動割当て
設定の変更は、vSphere Web Clientから行うか、vpxd.cfgから行います。
#### VMware OUI
これがデフォルトの設定ですが、00:50:56:{XX}:{YY}:{ZZ} という割当てを行います。
ただし、XX = {vCenterのid} + 0x80 で決めています。
そういうわけで、XXはvCenterごとに固定なので、65536個だけ利用可能だということになります。

普通は、こんなにMACアドレスを使う前に、他の上限値(VM作成上限数やvCPU上限など)にぶち当たって悲しみを抱えるので、大丈夫だと思われます。
複数のvCenterを利用している人は、vCenter間でIDがかぶっていないことは確認する必要があります。

この割当て方式では、00:50:56:80:{YY}:{ZZ} - 00:50:56:BF:{YY}:{ZZ} までの範囲が割当てられるので、見ればわかります。

以下が vpxd.cfgでの例です。

```xml
<vpxd>
<macAllocScheme>
<VMwareOUI>true</VMwareOUI>
</macAllocScheme>
</vpxd>
```

#### プレフィックスベース

5.1以降の環境では、デフォルトの00:50:56以外のプレフィックスを指定できます。
また、個数が足りない時には LAA(ローカル管理アドレス)プレフィックスを使うこともできます。
自分のOUIを使いたいときとか、複数vCenterがある時にLAA使う場合に使いそうです。

以下の設定は、00:50:26または、00:50:27から始まるMACアドレスを割当てる例です。

```xml
<vpxd>
<macAllocScheme>
<prefixScheme>
<prefix>005026</prefix>
<prefixLength>23</prefixLength>
</prefixScheme>
</macAllocScheme>
</vpxd>
```

#### 範囲ベース

開始と終了のMACアドレスを指定するものです。
LAAの複数の範囲を指定できるので、便利かもしれません。

これも複数vCenterを使うときには、分割して使えるので便利だと思います。

たぶん、こっちの方が、後で拡張したいときには便利なので、(そんなことあるのか知らないけど、)自由に使えるMACアドレス数が少ない場合には、後で追加しやすくて便利だと思います。

以下が、範囲ベース割当ての例です。 range idは0から始まります。 以下の例では、00:50:67:00:00:01のみの範囲1つだけを利用する例です。

```xml
<vpxd>
<macAllocScheme>
<rangeScheme>
<range id="0">
  <begin>005067000001</begin>
  <end>005067000001</end>
</range>
</rangeScheme>
</macAllocScheme>
</vpxd>
```
### vCenterに接続されていないESXiにより自動割当て
これが利用されるのは、
1. vCenterに接続されていない
2. vmxファイルに、MACアドレスやMACアドレス割当てタイプが書かれていない
場合です。

割当てられるMACアドレスは 00:0C:29 + {UUIDの最後の3オクテット} です。

### 固定割当て
デフォルトのOUIは 00:50:56 です。
このOUIを利用する場合、上で見たように他の用途で使われる箇所は予約されています。そのため、 00:50:56:00:{YY}:{ZZ} - 00:50:56:3F:{YY}:{ZZ} のみが利用可能です。

これを利用するためには、以下を削除して、

```
ethernetN.generatedAddress
ethernetN.addressType
ethernetN.generatedAddressOffset
```

以下を記述します。

```
ethernetN.addressType = static
ethernetN.address     = {MAC ADDRESS}
```

## 3. MACアドレスが足りなくなった時の動作

起動されるときに、MACアドレスが生成されます。
基本的には、起動中のMACアドレスとの衝突しか検知しないので、仮想マシンを一時的に停止している場合、再起動したときに、たまにMACアドレスが変更されてしまうことがありえます。

## 4. 資料
vSphere ネットワークガイド
- MACアドレスの管理
