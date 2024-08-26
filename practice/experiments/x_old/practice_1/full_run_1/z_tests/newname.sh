#!/bin/bash

for n in $(ls -p | grep -v /); do 
    #num=$(n | sed -r's/[a-zA-Z]/X/g' -e 's/[0-9]/N/g')
    #num=$(echo $n | sed -r 's/(\d+)\D*\z'/\1/ )
    #mv tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_20_startNudge_ track_0$n.mp3
    #echo "$num"

    #[[ $n =~ (\d+)\D*\z  ]]
    [[ $n =~ ([0-9]+)  ]]
    #[[ $n =~ .*(?:\D|^)(\d+)  ]]
    #[[ $n =~ ([0-9]+)\z  ]]

    echo "${BASH_REMATCH[1]}"
    #echo ${BASH_REMATCH[2]}

done

#for i in *; do 
#    if [[ $i =~ (image_)([0-9]{1,2})(\.jpg) ]]; then 
#        printf -v num "%03d" "${BASH_REMATCH[2]}"; 
#        echo mv -v "$i" "${BASH_REMATCH[1]}${num}${BASH_REMATCH[3]}"; 
#    fi; 
#done


#rename -n 's/(\d+)(?=.*\.)/sprintf("%04d",$1)/eg' *

#rename 's/\d+/sprintf("%04d",$&)/e' *.txt


#expr="tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_20_startNudge_6520.nc"
#num=`expr match "$3" '(\d+)(\D+)'`
#paddednum=`printf "%05d" $num`
#echo ${1/$num/$paddednum}


#shopt -s nullglob  # Patterns that match nothing expand to nothing.
#
#for f in [0-9][0-9][0-9].* ; do
#    mv "$f" "0$f"
#done
