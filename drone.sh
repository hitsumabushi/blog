#!/usr/bin/env bash

set -x

pip install -r requirements.txt --use-mirrors

make clean
make html
git checkout -b gh-pages

cp -r output/* .

rm -r content
rm -r output
rm *.sh
rm *.py
rm Makefile
rm *.txt
rm .gitignore

git add -A .
git commit -m "build by drone.io"
git remote set-url origin git@github.com:hitsumabushi/blog.git
git push -f origin gh-pages

