# Datacube Ingestion Scheduler

from ConfigParser import ConfigParser
from entities.LockFile import LockFile
from entities.Connection import Connection
from entities.Executions import Executions
from exceptions import Exception
import os, sys, datetime, glob, traceback

CONF_FILE = 'settings.conf'

conf = ConfigParser()
conf.read(CONF_FILE)

FLOWER = conf.get('flower','url')

lockfile = LockFile(conf.get('other','lock_file'))
if lockfile.search():
	print 'There\'s an execution in progress'
	sys.exit(1)
else:
	lockfile.write()

try:
	print 'DATACUBE EXECUTION MONITOR'

	dbconn = Connection(
				host=conf.get('database','host'),
				port=conf.get('database','port'),
				name=conf.get('database','name'),
				user=conf.get('database','user'),
				password=conf.get('database','password')
				)

	dbconn.connect()

	executions = Executions(dbconn.curr_conn, FLOWER)
	executions.load_enqueued_executing()

	for each_execution in executions.executions:
		print str(each_execution._id) + '. ' + each_execution.description + ' - state: ' + each_execution.state
		for each_task in each_execution.tasks.tasks:
			print '\t' + str(each_task._id) + ' - ' + str(each_task.uuid) + ' - ' + str(each_task.state) + ' - ' + str(each_task.end_date)

except Exception as e:
	traceback.print_exc()
finally:
	lockfile.delete()
	dbconn.close()
