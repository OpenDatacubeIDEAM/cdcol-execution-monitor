#!/bin/bash

NETCDF_PATH=$1
GRID_FILE_VAR=''
GRID_FILE=$NETCDF_PATH/grid.txt

XSIZE=0
YSIZE=0
xsize_list=''
ysize_list=''

# $1 = Variable name
# $2 = Variable value
function set_var {
	GRID_FILE_VAR=$(echo "$GRID_FILE_VAR" | sed -e "s/\(^$1[ ]*=\).*$/\1 $2/")
}

function get_var {
	echo "$1" | grep $2 | sed -e "s/^[^=]*=[ ]*\([^ ]*\).*$/\1/"
}

function sum_list {
	SUM=0
	for each_num in $1
	do
		SUM=$(echo "$SUM + $each_num" | bc)
	done
	echo $SUM
}

FIRST_FILE=true

for each_file in $(ls $NETCDF_PATH/*.nc)
do
	if [ $FIRST_FILE = true ]
	then
		GRID_FILE_VAR=$(cdo griddes $each_file | grep -E '^[^=]*=[^=]*$')
		FIRST_FILE=false
	fi
	cdo_griddes=$(cdo griddes $each_file)
	xsize_list="$xsize_list;$(get_var "$cdo_griddes" xfirst) $(get_var "$cdo_griddes" xsize)"
	ysize_list="$ysize_list;$(get_var "$cdo_griddes" yfirst) $(get_var "$cdo_griddes" ysize)"
done

xsize_list="$(echo $xsize_list | sed -e 's/;/\n/g' | sort -t ' ' -u -n -k 1)"
ysize_list="$(echo $ysize_list | sed -e 's/;/\n/g' | sort -t ' ' -r -u -n -k 1)"

XFIRST="${xsize_list%% *}"
YFIRST="${ysize_list%% *}"

xsize_list="$(echo "$xsize_list" | cut -d ' ' -f 2)"
ysize_list="$(echo "$ysize_list" | cut -d ' ' -f 2)"

XSIZE=$(sum_list "$xsize_list")
YSIZE=$(sum_list "$ysize_list")

GRID_SIZE=$(echo "$XSIZE * $YSIZE" | bc)

set_var gridsize "$GRID_SIZE"
set_var xsize "$XSIZE"
set_var ysize "$YSIZE"
set_var xfirst "$XFIRST"
set_var yfirst "$YFIRST"

echo "$GRID_FILE_VAR" > $GRID_FILE