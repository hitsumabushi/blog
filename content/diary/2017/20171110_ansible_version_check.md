Title: Ansible でバージョンチェックする
Date: 2017-11-10 14:02
Category: blog
Tags: ansible,debian

[TOC]

# やりたいこと
サーバー管理には ansible を使っていますが、apt で入れているパッケージに対して、以下をやりたい状況がありました。
- インストールされていなかったらインストール
- あるバージョン未満だったらアップデート

pipやgemといった言語のパッケージマネージャと違って、apt ではバージョンの制約を書くことが面倒です。
いい感じに playbook の中でバージョン比較をして、インストール/アップデートすべきかを判定したいと考えました。

# 結論

* バージョン比較には、 `version_compare` filter を使う
    - [Version Comparison](http://docs.ansible.com/ansible/latest/playbooks_tests.html#version-comparison)
* バージョン比較方法としては、 `LooseVersion` と `StrictVersion` がある
* 実装としては、 python の `distutils.version` を利用しているので、どう判定されるか迷ったら、比較してみれば良い

## playbook

例えば、docker の場合だと、以下のような感じで書けば良い。

```yaml
# docker version を取得
# docer version してみて、
#   - rc が 1 だったら、docker がインストールされていないと判断
#   - stdout にバージョンが入る
- name: check docker version
  command: docker version -f \{\{.Server.Version\}\}
  changed_when: false
  ignore_errors: yes
  register: docker_installed

- name: install curl
  apt: name=curl

- name: install docker
  shell: curl -sSL https://get.docker.com/ | sudo sh
  when: docker_installed.rc == 1

# docker_min_version という変数が定義されているとする。
# 例えば、 '1.11.0' という文字列が入っている
- name: update docker if older than docker_min_version
  apt: name=docker-engine state=latest
  when: docker_installed.stdout | version_compare(docker_min_version,  '<')
```

## distutils.version で試してみる

```pycon
>>> from distutils.version import LooseVersion
>>> LooseVersion('1.10.3') < LooseVersion('1.11.0')
True
>>> LooseVersion('17.05.0-ce') < LooseVersion('1.11.0')
False
```
