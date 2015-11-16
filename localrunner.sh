#!/usr/bin/sh

rm -rf tunirtests
mkdir -p tunirtests
cp -f *.py tunirtests/
cp LICENSE tunirtests
mkdir -p /tmp/localrunner
tar -czvf /tmp/localrunner/tunirtests.tar.gz tunirtests
cd /tmp/localrunner
python -m SimpleHTTPServer
