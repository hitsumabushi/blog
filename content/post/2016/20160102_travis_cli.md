---
title: Travis コマンドでのエラー
date: 2016-01-02T15:13:00+09:00
slug: '1513'
categories:
  - blog
tags:
  - travis
---


Travis CIでCIする素振りをしていたら、最新版のtravisコマンドでエラーが出るようになった。

## 発生した問題

```sh
$ travis setup releases
Invalid scheme format: git@github.com
for a full error report, run travis report
```

## 問題の解析

こういう時には、
```sh
$ travis report
```
をして、スタックトレースを見るものらしい。

```sh
$ travis report
System
Ruby:                     Ruby 2.3.0-p0
Operating System:         Mac OS X 10.11.2
RubyGems:                 RubyGems 2.5.1

CLI
Version:                  1.8.0
Plugins:                  none
Auto-Completion:          yes
Last Version Check:       2016-01-02 14:54:05 +0900

Session
API Endpoint:             https://api.travis-ci.org/
Logged In:                as "<username>"
Verify SSL:               yes
Enterprise:               no

Endpoints
org:                      https://api.travis-ci.org/ (access token, current)

Last Exception
An error occurred running `travis setup`:
    Addressable::URI::InvalidURIError: Invalid scheme format: git@github.com
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/addressable-2.4.0/lib/addressable/uri.rb:867:in `scheme='
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/addressable-2.4.0/lib/addressable/uri.rb:795:in `block in initialize'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/addressable-2.4.0/lib/addressable/uri.rb:2302:in `defer_validation'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/addressable-2.4.0/lib/addressable/uri.rb:792:in `initialize'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/addressable-2.4.0/lib/addressable/uri.rb:135:in `new'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/addressable-2.4.0/lib/addressable/uri.rb:135:in `parse'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/travis-1.8.0/lib/travis/cli/repo_command.rb:71:in `detect_slug'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/travis-1.8.0/lib/travis/cli/repo_command.rb:60:in `find_slug'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/travis-1.8.0/lib/travis/cli/repo_command.rb:21:in `setup'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/travis-1.8.0/lib/travis/cli/command.rb:197:in `execute'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/travis-1.8.0/lib/travis/cli.rb:64:in `run'
        from /Users/<username>/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/travis-1.8.0/bin/travis:18:in `<top (required)>'
        from /Users/<username>/.rbenv/versions/2.3.0/bin/travis:23:in `load'
        from /Users/<username>/.rbenv/versions/2.3.0/bin/travis:23:in `<main>'


For issues with the command line tool, please visit https://github.com/travis-ci/travis.rb/issues.
For Travis CI in general, go to https://github.com/travis-ci/travis-ci/issues or email support@travis-ci.com.
```

見た感じ、addressable というモジュールでパースに失敗しているらしい。

`travis.gemspec` を見ると、確かに、 `addressable` というモジュールがあるけど、
```ruby
s.add_dependency "addressable",           "~> 2.3"
```
という指定になっている。一方で、上記のスタックトレースでは、`addressable-2.4.0` を使っているので、当たりをつけて以下を実行する。

```sh
$ gem uninstall  addressable
$ gem install -v2.3.8 addressable
```

これで、travis コマンドが正常に実行できるようになる。

### ISSUE上での話

というところまで来て、改めて、issueを見てみたところ、<https://github.com/travis-ci/travis.rb/issues/342> で議論されている。
結論としては、以下の通りで、現状はまだ未修正だった。
"`addressable`モジュールでは、URIをparseするためのライブラリだけど、SCP styleのURIというのは、RFCにもなってないので、`addressable`モジュールでサポートするものではないよ。なので、 travisコマンド側でハンドルしよう。"

