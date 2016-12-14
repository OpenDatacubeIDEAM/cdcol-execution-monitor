#!/bin/bash

EXEC_MON_FOLDER=$HOME/execution-monitor
PYTHON=$HOME/anaconda2/bin/python

echo "$(date) RUNNING EXECUTION MONITOR"
source $HOME/.bashrc
cd $EXEC_MON_FOLDER
$PYTHON run_monitor.py
echo "$(date) DONE"
