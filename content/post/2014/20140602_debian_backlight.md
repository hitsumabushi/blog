---
title: LEDバックライトの調整
date: 2014-06-02T16:31:00+09:00
slug: 1631
categories:
  - blog
tags:
  - Debian
  - Linux
---


ディスプレイの輝度が高すぎて目が痛いので、輝度を下げたい。
GUIでやっても良いけど、CLIの方が簡単そうだったので、CLIでやってみることにした。

## 環境
- PC: ASUS 24A
- OS: Linux(Debian sid amd64)

## 調整可能な範囲
```shell
  cat /sys/class/backlight/intel_backlight/max_brightness
```

## ディスプレイの明るさ変更
```shell
  # 明るさを800にするとき
  echo 800 | sudo tee /sys/class/backlight/intel_backlight/brightness
```

