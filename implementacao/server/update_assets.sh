#!/bin/bash

if [ ! -f "memes.zip" ]; then
  gdown --id 12x46KaDlY5d1OzXJtEERGDoEaI6bPV-O
  mkdir -p webdir/imagens/memes/
  unzip -u memes.zip -d webdir/imagens/
  rm memes.zip
fi

if [ ! -f "sons.zip" ]; then
  gdown --id 1b9W-7M-QltBvurp4cMXgWbvutJe-K7Uq
  mkdir -p webdir/sons/
  unzip -u sons.zip -d webdir/
  rm sons.zip
fi

if [ ! -f "videos.zip" ]; then
  gdown --id 1DLO1aRCZFgJZeGQoVnlQZpZLVuPHiZ4F
  mkdir -p webdir/videos/
  unzip -u videos.zip -d webdir/
  rm videos.zip
fi

if [ ! -f "trofeus.zip" ]; then
  gdown --id 14_cIOufhgvm01vlETuJrHB5WynAMFlrq
  mkdir -p webdir/trofeus/
  unzip -u trofeus.zip -d webdir/
  rm trofeus.zip
fi

gdown --id 1fDOrGiP1gqAUehyAOhZgRMwHyeVgiu81
mv premiacao.png webdir/imagens/lobby/banners/

gdown --id 15Y7Zrp9s4FiQuKgMiN-lxTad7xyEhh0l
mv premio.png webdir/imagens/lobby/banners/

gdown --id 1ld32cN6WSX61anUjnlGQd5GcESwxHK43
mv evento_chat.png webdir/imagens/lobby/banners/
