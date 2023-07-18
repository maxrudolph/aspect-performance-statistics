#!/bin/bash
set -x
cluster=peloton-ii-32tasks-ubuntu22
mkdir results/spherical_shell_expensive_solver/${cluster}
for i in `ls tmp/$cluster | grep output`
do
echo=1
j=`echo $i | cut -d _ -f 2-4`
cp tmp/$cluster/$i/log.txt results/spherical_shell_expensive_solver/${cluster}/output_$j
done
