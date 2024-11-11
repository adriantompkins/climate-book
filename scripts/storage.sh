#!/bin/bash

#dir=~/raid/simona
dir=/scratch/oayim/project/tcwv/new_tcwv
#dir1=/scratch/oayim/project/fam
dir2=/scratch/oayim/project/africa
#dir2=/scratch/oayim/project/sasm
year1=1987
year2=2019

#name=asia
#region="60,100,10,30"
#name=asia
#n=27
#s=5
#w=60
#e=100

#sn10_20_we-20_10
name=africa 
n=18
s=8
w=-20
e=30

#name=africa 
#n=20
#s=10
#w=-20
#e=10
region="$w,$e,$s,$n"
tag=sn${s}_${n}_we${w}_${e}

for year in $(seq $year1 $year2) ; do
#for year in $year1 ; do
rm -f $dir2/tmp*.nc
rm -f $dir2/ts*.nc
rm -f $dir2/outp*.nc
rm -f $dir2/tcwv_mean*.nc
rm -f $dir2/diff.nc*
rm -f $dir2/fin*
for mon in $(seq -w 01 12) ; do 
  file=$dir/tcwv_both_${year}${mon}.nc
  cdo -b 32 fldmean -sellonlatbox,${region} -daysum $file $dir2/tmp_mean_${name}_${year}${mon}.nc
 
done

cd africa

cdo mergetime -ydaymean tmp_mean_${name}_*.nc ts_mean_${name}_${tag}.nc
#cdo -mergetime tmp_mean_${name}_*.nc tcwv_mean_${name}_${tag}.nc

data=ts_mean_${name}_${tag}.nc
nstep=`cdo -s ntime $data`
cdo sub -seltimestep,2/$nstep $data -seltimestep,1/`expr $nstep - 1` $data diff.nc

#cdo mergetime -seltimestep,1 $data diff.nc output.nc 

cdo add evap_${year}_${name}_${tag}.nc vimd_${year}_${name}_${tag}.nc fin1.nc
cdo sub prec_${year}_${name}_${tag}.nc fin1.nc fin2.nc
cdo divc,1000 diff.nc storage_${year}_${name}_${tag}.nc #STORAGE
cdo add fin2.nc storage_${year}_${name}_${tag}.nc residual_${year}_${name}_${tag}.nc #RESIDUAL
cdo timmean storage_${year}_${name}_${tag}.nc mean_storage_${year}_${name}_${tag}.nc
cdo timcumsum -sub prec_${year}_${name}_${tag}.nc evap_${year}_${name}_${tag}.nc prec_evap_${year}_${name}_${tag}.nc
cd ..
echo $year 'done'
done 
#cdo add final_evap_${name}_${tag}.nc final_vimd_${name}_${tag}.nc fin_1.nc
#cdo sub final_prec_${name}_${tag}.nc fin_1.nc fin2.nc
#cdo divc,1000 diff.nc out.nc #STORAGE
#cdo add fin2.nc out.nc phone.nc #RESIDUAL
#cdo timmean out.nc mean_storage.nc








