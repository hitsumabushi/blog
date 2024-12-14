---
title: CloudFormation Stackを安全に削除する
date: 2021-10-12T02:00:00+09:00
slug: '0200'
aliases:
  - 0200.html
categories:
  - blog
tags:
  - aws
  - cloudformation
---


以前、[CloudFormation の不満点]({filename}/diary/2019/20190125_cloudformation_drift.md) というのを書いたが、諦めて大半のCfnをterraformに移行した。
その際、cfn リソースをきれいにするために、cfn stackを安全に削除する必要があり、その方法をメモしておく。

## 概要

アイデアは簡単で以下の通り。

1. cfn の操作のみが許可されているIAM roleを作成する
2. 上記roleを指定して cfn stackをdeleteする

## モチベーション

そもそも以前の記事でも、予期せぬ手作業の変更があった場合に、ドリフト検出やChange setで検出・対応が難しいことを問題としていた。
cfn stackを削除しようと思った場合、ドリフトしている状態だと、単純には削除できない。一旦cfn updateすれば簡単かもしれないが、何か手作業で変更されているかもしれない状況だと、updateしたくない。
cfn updateをせずに、安全にcfn stackをdeleteしたい。

## 方法

### cfnの操作しかできないIAM roleを作成する

以下の通り、terraformで作成した。

```terraform
resource "aws_iam_role" "delete_cfn_stack" {
  name = "delete-cfn-stack"
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "cloudformation.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "delete_cfn_stack_policy" {
  name = "cfn_policy"
  role = aws_iam_role.delete_cfn_stack.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "cloudformation:*",
        ]
        Resource = "*"
      },
    ]
  })
}
```

### 上記のroleでスタック削除する

```sh
export STACK_NAME=stack_name

# 失敗するdeleteを実行
aws cloudformation delete-stack --role-arn arn:aws:iam::_aws_account_id_:role/delete-cfn-stack --stack-name ${STACK_NAME}

# resource idのリストを取得
aws cloudformation describe-stack-resources --stack-name ${STACK_NAME} | jq '.StackResources[].LogicalResourceId' | xargs

# 削除しないリソースとして上の結果を指定
aws cloudformation delete-stack --role-arn arn:aws:iam::_aws_account_id_:role/delete-cfn-stack --stack-name ${STACK_NAME} --retain-resources (↑の結果をペースト)
```

## 終わり

地道にterraform importしてから、上記をコツコツ(スクリプト化して)実行して、cfn stackを削除した。
terraform importは単純に差分がなくなるまでtf fileを修正するだけなので、そんなに困ることはない。
これで安心・安全にリソース管理できるようになった。