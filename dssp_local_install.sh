#!/bin/bash
# make local installation of DSSP
  
tar -zxvf dssp-2.3.0.tar.gz
cd dssp-2.3.0
./autogen.sh
./configure
make
make mkdssp
sudo make install
cd ../
mkdssp --version
