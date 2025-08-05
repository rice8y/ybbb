#!/bin/bash

mkdir -p tmp-ybbb && cd tmp-ybbb
git clone https://github.com/rice8y/ybbb.git
uv tool install -e ./bench
cd ../ && rm -rf tmp-ybbb