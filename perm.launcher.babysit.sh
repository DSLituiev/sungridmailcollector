#!/usr/bin/bash

jobnums="num.jobids.tab"
scriptname="run.rna.gt.gcta.sh"


oldIFS="$IFS"
IFS=$'\n' arr=($(<$jobnums))
IFS="$oldIFS"

line=${arr[1]}
cells=($line)

for line in "${arr[@]:1}"
do
    cells=($line)
    batch=${cells[0]}
    export permutations=${cells[1]}
    echo $batch , $permutations
    tmpscript="$scriptname.${permutations}"
    cat "$scriptname" | envsubst  '$permutations, ${batch}'> "$tmpscript" || exit 1
    echo $tmpscript >&2
    #exit 1
    qsub -t ${batch} $tmpscript || exit 1
    rm $tmpscript 
done

