#!/usr/bin/env bash
set -e

# resolv dependency
#pip install -r requirements.txt

# sync submodule
#git submodule init
#git submodule update

# build html
make clean
make html || exit 1

# git config
git config user.email "${GIT_USER_EMAIL}"
git config user.name "${GIT_USER_NAME}"

# checkout branch
git checkout -b gh-pages

# copy output to top of repository
cp -r output/* .

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
git commit -m "Build by Travis-CI"
git push -fq "https://${GITHUB_TOKEN}@github.com/hitsumabushi/blog.git" gh-pages:gh-pages > /dev/null 2>&1 # forced push

# For cloudflare : purge caches of all
#curl -X DELETE "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
#  -H "X-Auth-Email: ${CLOUDFLARE_AUTH_EMAIL}" \
#  -H "X-Auth-Key: ${CLOUDFLARE_AUTH_KEY}" \
#  -H "Content-Type: application/json" \
#  --data '{"purge_everything":true}'
# For cloudflare : purge caches of index.html
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
  -H "X-Auth-Email: ${CLOUDFLARE_AUTH_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_AUTH_KEY}" \
  -H "Content-Type: application/json" \
  --data "{\"files\":[\"${SITE_BASE_URL}/\", \"${SITE_BASE_URL}/index.html\", \"${SITE_BASE_URL}/archives.html\"]}" > /dev/null 2>&1
