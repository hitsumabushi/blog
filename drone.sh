#!/usr/bin/env bash
set -x

# resolv dependency
pip install -r requirements.txt --use-mirrors

# sync submodule
git submodule update

# build html
make clean
make html

# checkout branch
git checkout -b gh-pages

# copy output to top of repository
cp -r output/* .

# Remove unpublish files
rm -r content
rm -r output
rm *.sh
rm *.py
rm Makefile
rm requirements.txt
rm .gitignore
rm -rf themes/*
rm -rf __pycache__
rm -rf cache

# Git push
git add -A .
git commit -m "Build by drone.io"
git remote set-url origin git@github.com:hitsumabushi/blog.git
git push -f origin gh-pages  # forced push

