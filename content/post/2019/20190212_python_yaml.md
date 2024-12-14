---
title: Python でコメント付きYAMLを扱う時には ruamel.yaml が便利だった
date: 2019-02-12T16:30:00+09:00
slug: '1630'
aliases:
  - 1630.html
categories:
  - blog
tags:
  - python
  - yaml
---



## 資料

* [Document: ruamel.yaml](https://yaml.readthedocs.io/en/latest/)
* [Repository: ruamel.yaml](https://bitbucket.org/ruamel/yaml/)

## 背景

とある yamlで書かれたconfigファイル群(数百ファイル)を一括で変更したいことがあった。
sedで変更するには少し難しかったので、パースしてから条件判定して、書き換えたい。

* コメントは消したくない
* ブロックスタイルのままにしたい
* diff を最小限にしたい (細かい中身を知らないので、チェックするのが面倒)

## ruamel.yaml

python で yaml を扱うときは、PyYAML が有名だと思う。
PyYAMLを使う場合、yamlをloadしてdumpすると、フロースタイルなのは変更できるが、
コメントは消えてしまうのに対応するのが簡単ではない(と思っている)。

ruamel.yaml はPyYAMLをフォークしたもので、YAML 1.2 をサポートしているし、コメントやスタイル、キーの順番を保つloaderが実装されている。
https://yaml.readthedocs.io/en/latest/overview.html

### 使い方

使い方としては、 load, dumpの代わりに、 `round_trip_load`, `round_trip_dump` を使えば良い。
オプションは自分が使っているconfigに合わせて使えば良い。

```python
import ruamel.yaml
import os

def process(filepath):
    with open(filepath, 'r+') as f:
        data = ruamel.yaml.round_trip_load(f, preserve_quotes=True)
        # 必要な処理をする
        # data["foo"] = "bar"
        if rewrite:
            f.seek(0)
            ruamel.yaml.round_trip_dump(data, f, explicit_start=True)
            f.truncate()

for pathname, dirnames, filenames  in os.walk('.'):
    for filename in filenames:
        print(f"{pathname}/{filename}")
        process(f"{pathname}/{filename}")
```
