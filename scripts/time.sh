#!/bin/bash

#dir=~/raid/simona

year1=2000
#year2=2001

#name=asia
#region="60,100,10,30"

name=asia 
n=30
s=10
w=60
e=100
region="$w,$e,$s,$n"
tag=sn${s}_${n}_we${w}_${e}
rm -f tmp*.nc
rm -f ts*.nc
rm -f outp*.nc
rm -f tcwv_mean*.nc
#rm -f cum*

for year in $year1 ; do 
for mon in $(seq -w 01 12) ; do 
  file=tcwv_both_${year}${mon}.nc
  cdo -b 32 fldmean -sellonlatbox,${region} -daysum $file tmp_mean_${name}_${year}${mon}.nc
 
done

done 

#cdo ydaymean -mergetime tmp_mean_${name}_*.nc ts_mean_${name}_${tag}.nc
cdo -mergetime tmp_mean_${name}_*.nc tcwv_mean_${name}_${tag}.nc

data=tcwv_mean_${name}_${tag}.nc
nstep=`cdo -s ntime $data`
cdo sub -seltimestep,2/$nstep $data -seltimestep,1/`expr $nstep - 1` $data diff.nc

cdo mergetime -seltimestep,1 $data diff.nc output.nc 

#cdo add final_evap_${name}_${tag}.nc -sub final_prec_${name}_${tag}.nc -add output.nc final_vimd_${name}_${tag}.nc residual.nc

#cdo seltimestep,2/366 residual.nc res.nc
#final_prec_${name}_${tag}.nc final_evap_${name}_${tag}.nc final_vimd_${name}_${tag}.nc
cdo add final_evap_${name}_${tag}.nc final_vimd_${name}_${tag}.nc fin_1.nc
cdo sub final_prec_${name}_${tag}.nc fin_1.nc fin2.nc
cdo divc,1000 diff.nc out.nc #STORAGE
cdo add fin2.nc out.nc phone.nc #RESIDUAL
cdo timmean out.nc mean_storage.nc

