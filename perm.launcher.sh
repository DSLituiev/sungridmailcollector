#!/usr/bin/bash

scriptname="./run.rna.ca_05.lm.sh"
for nn in `seq 1 10`
do
    export permutations=$nn
    tmpscript="$scriptname.${permutations}"
    cat "$scriptname" | envsubst  '$permutations'> "$tmpscript" || exit 1
    qsub $tmpscript || exit 1
    echo $tmpscript >&2
    rm $tmpscript 
done

