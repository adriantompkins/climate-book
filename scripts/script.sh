#!/bin/bash

dir=/scratch/oayim/project/data
dir1=/scratch/oayim/project/full

year1=1987
year2=2019

#name=asia
#n=27
#s=5
#w=60
#e=100


name=africa 
n=20
s=10
w=-20
e=40
#region="$w,$e,$s,$n"

tag=sn${s}_${n}_we${w}_${e}
region="$w,$e,$s,$n"
#region="60,100,10,30"

for year in $(seq $year1 $year2) ; do 
#for year in $year1; do 
rm -f $dir1/ts_mean_${name}_${tag}.nc
rm -f $dir1/tmp*.nc

for mon in $(seq -w 01 12) ; do 
  file=$dir/flux_both_${year}${mon}.nc
  cdo -b 32 fldmean -sellonlatbox,${region} -daysum $file $dir1/tmp_mean_${name}_${year}${mon}.nc
done



#cdo -b 32 mergetime $dir/tmp_mean_${name}_*.nc $dir/ts_mean_${name}_${tag}.nc

cdo mergetime -ydaymean $dir1/tmp_mean_${name}_*.nc $dir1/ts_mean_${name}_${tag}.nc

cdo mulc,1000 -selvar,tp $dir1/ts_mean_${name}_${tag}.nc $dir1/prec_${year}_${name}_${tag}.nc
cdo mulc,-1000 -selvar,e $dir1/ts_mean_${name}_${tag}.nc $dir1/evap_${year}_${name}_${tag}.nc
cdo mulc,-1 -selvar,vimd $dir1/ts_mean_${name}_${tag}.nc $dir1/vimd_${year}_${name}_${tag}.nc
cdo timcumsum $dir1/vimd_${year}_${name}_${tag}.nc $dir1/cum_vimd_${year}_${name}_${tag}.nc 
done 
#cdo -b 32 timcumsum $dir/ts_mean_${name}_${tag}.nc $dir/cs_mean_${name}_${tag}.nc


