---
title: PyPIへパッケージをアップロードする
date: 2018-04-05T14:20:00+09:00
slug: 1420
categories:
  - blog
tags:
  - pypi
  - python
---



# 資料

* パッケージ構成については [github.com/pypa/sampleproject](https://github.com/pypa/sampleproject)
* https://pypi.python.org/pypi/twine
* https://packaging.python.org/tutorials/distributing-packages/

# 手順

## PyPIへユーザー登録する

PyPI には普段使われている本番環境とは別に、テスト環境がある。
アカウントがそれぞれ独立しているので、両方で作成する必要がある。

* [PyPI](https://pypi.org/)
* [PyPI Test](https://test.pypi.org/)

## `.pypirc` の作成

以下のように `~/.pypirc` を作成して、test 環境を利用できるようにしておく。
平分でパスワードを書くことになるので、最低限パーミッションを変えておくことにする。

```
$ cat ~/.pypirc
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
repository=https://upload.pypi.org/legacy/
username=_username_
password=_password_

[testpypi]
repository=https://test.pypi.org/legacy/
username=_username_
password=_password_

$ chmod 0600 ~/.pypirc
```

## パッケージのアップロード

### コマンドのインストール

```
$ pip install twine
```

### パッケージング前のチェック

```
$ pip install check-manifest
$ check-manifest
```

### パッケージング

```
$ pip install wheel
$ python setup.py sdist bdist_wheel
```

### Test 環境へアップロード

```
$ twine upload -r testpypi dist/*
```

pip でインストールするには、以下のようにする。

```
$ pip install --index-url https://test.pypi.org/simple/ _package_
```

### 本番へアップロード

```
$ twine upload dist/*
```
