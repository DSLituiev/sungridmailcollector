#!/usr/bin/bash

jobnums="notebooks/missing_weightedglmnet_all_imputed_cov_pcs4ca_orth_gt_new_atac_peaks_std_1r_0_500_centre_window2e4_cvfold5.list"
scriptname="run.ca.gt.glmnet.sh"


oldIFS="$IFS"
IFS=$'\n' arr=($(<$jobnums))
IFS="$oldIFS"

for ii in ${arr[@]}
do
    #echo $ii
    qsub -t $ii $scriptname
done


