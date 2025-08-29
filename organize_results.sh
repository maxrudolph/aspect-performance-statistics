#!/bin/bash
set -x
<<<<<<< HEAD
cluster=peloton-ii-32tasks-core-openmpi-4.0.1
=======
cluster=peloton-ii-32tasks-ubuntu22
>>>>>>> 92aaed7763c3e0cec298a5d5035264c1ad434373
mkdir results/spherical_shell_expensive_solver/${cluster}
for i in `ls tmp/$cluster | grep output`
do
echo=1
j=`echo $i | cut -d _ -f 2-4`
cp tmp/$cluster/$i/log.txt results/spherical_shell_expensive_solver/${cluster}/output_$j
done
