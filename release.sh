#!/bin/bash
AVVY_CLIENT_COMMON_TMP=$AVVY_CLIENT_COMMON
unset AVVY_CLIENT_COMMON
python3 build.py

echo "Current version is $(cat VERSION.txt).  What version did you want to release?"
read VERSION
echo $VERSION > VERSION.txt
python setup.py sdist
(cd dist && twine upload "avvy-$VERSION.tar.gz")
git add .
git commit -m "v$VERSION"
git tag -a "v$VERSION" -m "v$VERSION"

