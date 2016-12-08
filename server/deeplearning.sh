#!/bin/bash

cp $1 ~/GitHub/darknet/test.jpg
cd ~/GitHub/darknet
./darknet nightmare cfg/vgg-conv.cfg vgg-conv.weights test.jpg 10
mv test_vgg-conv_10_000000.png ~/hendigi_camera/server/$1
