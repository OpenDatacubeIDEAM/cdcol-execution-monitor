# Datacube Ingestion Scheduler

from ConfigParser import ConfigParser
from entities.LockFile import LockFile
from entities.Connection import Connection
from entities.Executions import Executions
from exceptions import Exception
import os, sys, datetime, glob

CONF_FILE = 'settings.conf'

conf = ConfigParser()
conf.read(CONF_FILE)

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

	executions = Executions(dbconn.curr_conn)
	executions.load_enqueued_executing()

	for each_execution in executions.executions:
		print str(each_execution._id) + '. ' + each_execution.description
		for each_task in each_execution.tasks.tasks:
			print '\t' + str(each_task._id) + ' - ' + str(each_task.uuid) + ' - ' + str(each_task.execution_id)

except Exception as e:
	print 'Error: ' + str(e)
finally:
	lockfile.delete()
