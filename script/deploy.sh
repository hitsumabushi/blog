#!/usr/bin/env bash
set -e

# resolv dependency
pip install -r requirements.txt --use-mirrors

# sync submodule
git submodule init
git submodule update

# build html
make clean
make html || exit 1

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
git commit -m "Build by Travis-CI"
git remote set-url origin git@github.com:hitsumabushi/blog.git
git push -f origin gh-pages  # forced push

# For cloudflare : purge caches
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
  -H "X-Auth-Email: ${CLOUDFLARE_AUTH_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_AUTH_KEY}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
