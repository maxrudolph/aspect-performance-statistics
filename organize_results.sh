#!/bin/bash

cluster=PI4CS_COEUS_aspect_2.0-pre
mkdir results/spherical_shell_expensive_solver/${cluster}
for i in `ls tmp | grep output`
do
j=`echo $i | cut -d _ -f 2-4`
cp tmp/$i/log.txt results/spherical_shell_expensive_solver/${cluster}/output_$j
done
