#!/bin/bash

dir=~scratch/oayim/project/data
dir1=~scratch/oayim/project/fameye

year1=2000
year2=2001

name=asia
region="60,100,10,30"

#name=africa 
#n=18
#s=8
#w=-20
#e=30
region="$w,$e,$s,$n"
tag=sn${s}_${n}_we${w}_${e}
rm -f $dir/tmp*.nc


for year in $(seq $year1 $year2) ; do 
for mon in $(seq -w 01 12) ; do 
  file=$dir/flux_both_${year}${mon}.nc
  cdo -b 32 fldmean -sellonlatbox,${region} -daysum $file $dir1/tmp_mean_${name}_${year}${mon}.nc
done
done 


#cdo -b 32 mergetime $dir/tmp_mean_${name}_*.nc $dir/ts_mean_${name}_${tag}.nc

cdo ydaymean -mergetime $dir1/tmp_mean_${name}_*.nc $dir1/ts_mean_${name}_${tag}.nc

cdo mulc,1000 -selvar,tp ts_mean_${name}_${tag}.nc tryout.nc

#cdo -b 32 timcumsum $dir/ts_mean_${name}_${tag}.nc $dir/cs_mean_${name}_${tag}.nc


