Title: kubernetes instal step
Date: 2017-10-24 01:54
Category: blog
Tags: kubernetes,docker,debian
Status: draft

[TOC]

# kubectl をインストール

kubernetes の管理に使うので、 kubectl をインストール

```
$ curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x ./kubectl
```

実行できるか確認する。
```
$ kubectl version --client -o yaml
clientVersion:
  buildDate: 2017-10-11T23:27:35Z
  compiler: gc
  gitCommit: f38e43b221d08850172a9a4ea785a86a3ffa3b3a
  gitTreeState: clean
  gitVersion: v1.8.1
  goVersion: go1.8.3
  major: "1"
  minor: "8"
  platform: linux/amd64
```

# local で k8s を立てる
## minikube をインストール

最新バージョンを確認してダウンロードする

```
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.22.3/minikube-linux-amd64 && chmod +x minikube
```

実行できるか確認する。
```
$ minikube version
minikube version: v0.22.3
```

## k8s cluster を作る

```
$ minikube start
Starting local Kubernetes v1.7.5 cluster...
Starting VM...
Downloading Minikube ISO
 139.09 MB / 139.09 MB [============================================] 100.00% 0s
Getting VM IP address...
Moving files into cluster...
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
```
```
$ kubectl get nodes
NAME       STATUS    ROLES     AGE       VERSION
minikube   Ready     <none>    1m        v1.7.5
```

## minikube ちょっと触る
* minikube dashboard
* minikube status
* minikube ip
* minikube ssh
* minikube docker-env

## 

```
$ kubectl run ghost --image=ghost:latest
deployment "ghost" created
$ kubectl expose deployments ghost --port=2368 --type=NodePort
service "ghost" exposed
$ kubectl get pods
NAME                     READY     STATUS    RESTARTS   AGE
ghost-1604807603-ttz54   1/1       Running   0          2m
```

expose したサービスをブラウズで開くのは minikube でできる。
```
$ minikube service ghost
```


状態を見る
```
$ kubectl get pods,rs,deployments
NAME                        READY     STATUS    RESTARTS   AGE
po/ghost-1604807603-ttz54   1/1       Running   0          11m
po/redis-2048254088-kmz83   1/1       Running   0          3m

NAME                  DESIRED   CURRENT   READY     AGE
rs/ghost-1604807603   1         1         1         11m
rs/redis-2048254088   1         1         1         3m

NAME           DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deploy/ghost   1         1         1            1           11m
deploy/redis   1         1         1            1           3m

$ kubectl logs redis-2048254088-kmz83
1:C 24 Oct 15:53:00.672 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 24 Oct 15:53:00.672 # Redis version=4.0.2, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 24 Oct 15:53:00.672 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
1:M 24 Oct 15:53:00.675 * Running mode=standalone, port=6379.
1:M 24 Oct 15:53:00.675 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
1:M 24 Oct 15:53:00.675 # Server initialized
1:M 24 Oct 15:53:00.675 * Ready to accept connections
```

