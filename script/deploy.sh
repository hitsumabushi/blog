#!/usr/bin/env bash
set -e

# build html
make clean
make html || exit 1

# git config
git config user.email "action@github.com"
git config user.name "GitHub Actions"

# checkout branch
git checkout -b gh-pages

# copy output to top of repository
cp -r output/* .
cp -r output/.* .

# Remove unpublish files
rm -rf content \
  output \
  script \
  plugins \
  themes \
  __pycache__ \
  cache

rm -f *.py \
  Makefile \
  requirements.txt \
  .gitmodules \
  .travis.yml

# Git push
git add -A .
git commit -m "Build by GitHub Actions"
git push -fq origin gh-pages

# For cloudflare : purge caches of all
# For cloudflare : purge caches of index.html
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
  -H "X-Auth-Email: ${CLOUDFLARE_AUTH_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_AUTH_KEY}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' > /dev/null 2>&1
