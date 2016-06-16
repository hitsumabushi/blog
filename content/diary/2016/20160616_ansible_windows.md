Title: Anisble for Windows
Date: 2016-06-16 06:02
Category: blog
Tags: ansible, windows

[TOC]

久しぶりに ansible で windows を操作するので、メモ。
実行側は Debian Sid でやっているので、apt-get しているところについては、適宜置き換えて欲しい。
ansibleは2.1.0を使っている。

# やること

以下を anisble で実行する。

1. Windows Update
2. Windows Server 2012 R2 に AD をインストール
3. ADに適当なダミーエントリを突っ込む

# 初期設定

## ansible 実行サーバーの準備

winrm経由で実行することになるので、 `pywinrm` が必要。

```
# pip install ansible pywinrm
```

## Inventory

```
[windows_server]
ad-seed-001 ansible_host=164.70.5.244

[windows_server:vars]
ansible_user=adminuser
ansible_port=5986
ansible_password=<password>
ansible_connection=winrm
ansible_winrm_server_cert_validation=ignore
```

## 接続確認

```
# ホスト側のwinrmの初期設定を行っていないと、おそらく失敗する
ansible -i inventory_file all -m win_ping
```

## ホスト側の初期設定

以下のスクリプトを実行すれば、ひとまずは、上記のpingが通る。
FWがパブリック/プライベートの両方空いたりするので、必要に応じてスクリプトを変更する。

https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1

再度、接続確認を行えば、おそらく成功する。

```
ansible -i inventory_file all -m setup
```
などとして、factを確認しておくと便利。


# ansible playbook

ある程度できたら書きます。

# 資料
- <http://docs.ansible.com/ansible/intro_windows.html>
- http://qiita.com/yunano/items/8bddf084007671a38f57 : スクリプトなどはこちらを参考にした
