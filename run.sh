#!/bin/bash

echo "$(date) RUNNING EXECUTION MONITOR"
source $HOME/.bashrc
cd $HOME/execution-monitor
$HOME/anaconda2/bin/python run_monitor.py
echo "$(date) DONE"
