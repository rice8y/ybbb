#!/bin/bash

git clone https://github.com/rice8y/ybbb.git
cd ybbb/bench
uv tool install -e .
cd ../../ && rm -rf ybbb