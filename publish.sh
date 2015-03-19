#!/usr/bin/sh

mkdir -p tunirtests
cp *.py tunirtests/
cp LICENSE tunirtests
tar -czvf /tmp/tunirtests.tar.gz tunirtests
scp /tmp/tunirtests.tar.gz kushal@fedorapeople.org:./public_html/
