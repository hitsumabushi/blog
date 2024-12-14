---
title: WindowsをAnsibleで設定する
date: 2015-05-28T06:07:00+09:00
slug: 0607
categories:
  - blog
tags:
  - Windows
  - ansible
---


# 資料
[Windows Support — Ansible Documentation](http://docs.ansible.com/intro_windows.html)

# マシンの準備
## ansibleコマンドを実行するマシン

ansibleがすでに実行できる状況であれば、
```sh
pip install http://github.com/diyan/pywinrm/archive/master.zip#egg=pywinrm
pip install kerberos # AD accountを使う場合
```
とすればOK。

## Windowsマシン
### 要件
1. WinRM がインストール済み
2. PowerShell version > 3.0
  - 自動的に、Windows 7SP1, Windows Server2008 SP1以降になる
  - Windows Server 2012ははじめからPowershell 4.0がインストールされている

### セットアップ方法
1. [Powershell 3.0にアップデートが必要な場合](https://github.com/cchurch/ansible/blob/devel/examples/scripts/upgrade_to_ps3.ps1)
2. [WinRMのインストール](https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1)
3. `Configure-SMRemoting.exe -get` で有効になっていることを確認
4. `WinRM get WinRM/config` でWinRMのポートを確認

# ansibleの実行方法
## Inventory
最小構成は以下の通り。 以降は、hostsという名前で呼ぶ。
```
[windows]
hostname

[windows:vars]
ansible_ssh_user=administrator
ansible_ssh_pass=_password_
ansible_ssh_port=5986
ansible_connection=winrm
```

## 利用可能なモジュール
1. raw, script, slurpなど
2. [Windows用のモジュール](http://docs.ansible.com/list_of_windows_modules.html)
  [この辺](https://github.com/ansible/ansible-modules-core/tree/devel/windows)にあるやつはできそう

# windows machineの facts
`ansible -i hosts _hostname_ -m setup` を実行する。

```
    "ansible_facts": {
        "ansible_distribution": "Microsoft Windows NT 6.3.9600.0",
        "ansible_distribution_version": "6.3.9600.0",
        "ansible_fqdn": "_FQDN_",
        "ansible_hostname": "_hostname_",
        "ansible_interfaces": [
            {
                "default_gateway": null,
                "dns_domain": null,
                "interface_index": 13,
                "interface_name": "vmxnet3 Ethernet Adapter #2"
            },
            {
                "default_gateway": "_GATEWAY_",
                "dns_domain": null,
                "interface_index": 14,
                "interface_name": "vmxnet3 Ethernet Adapter #3"
            }
        ],
        "ansible_ip_addresses": [
            "_local_ipv4_",
            "_local_ipv6_",
            "_global_ipv4_",
            "_global_ipv6_"
        ],
        "ansible_os_family": "Windows",
        "ansible_powershell_version": 4,
        "ansible_system": "Win32NT",
        "ansible_totalmem": 2147483648
    }
```

