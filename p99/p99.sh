#!/usr/bin/env bash

EQ_DIR=~/.wine32/drive_c/eq
EQ_MM=~/usr/src/p99-login-middlemand-master

function cleanup() {
  [ -n "$EQ_MM_PID" ] && kill $EQ_MM_PID
}

[ -d $EQ_DIR ] || exit 1
[ -d $EQ_MM ]  || exit 1

$EQ_MM/bin/p99-login-middlemand &
EQ_MM_PID=$!

trap cleanup INT EXIT

cd $EQ_DIR && VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/intel_icd.x86_64.json WINEPREFIX=~/.wine32 WINEARCH=win32 wine eqgame.exe patchme
