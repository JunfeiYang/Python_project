#!/bin/bash

time=`date +%Y年%m月%d日-%H时%M分%S秒`
git config --global user.name "kyadmin"
git config --global user.email "wyyservice@gmail.com"
cd ~/platform-manager
git add --all
git commit -m "I have pushed the code at $time "
git push -f
