#!/bin/bash

cd ../pgn

../bin/pgn-extract -Wuci --nocomments --nonags --novars --nobadresults "$1" | \
  ../bin/analyse --engine ../bin/stockfish --searchdepth 10 --annotatePGN | \
  ../bin/pgn-extract -Wsan --addhashcode --totalplycount -#1,100000

rm "$1"
