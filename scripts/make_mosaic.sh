
#!/bin/bash

NETCDF_PATH=$1
LOCK_FILE=$NETCDF_PATH/mosaic.lock
MAKE_MOSAIC_PY=/home/cubo/execution-monitor/scripts/make_mosaic.py
PYTHON=/home/cubo/anaconda2/bin/python
NETCDF_LIST=''
for each_file in $(ls $NETCDF_PATH/*_*.nc)
do
        NETCDF_LIST="$NETCDF_LIST ${each_file##*_}"
done
for each_suffix in $(echo $NETCDF_LIST | sed -e 's/ /\n/g' | sort -u)
do
        echo "$PYTHON $MAKE_MOSAIC_PY $NETCDF_PATH $each_suffix"
        $PYTHON $MAKE_MOSAIC_PY $NETCDF_PATH $each_suffix
done
echo done > $LOCK_FILE

