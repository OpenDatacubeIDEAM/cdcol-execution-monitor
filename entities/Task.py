from dao.Task import Task as DAOTask
from urllib2 import urlopen
import datetime, json

class Task():

	STATES= {
			'PENDING':'1',
			'RECEIVED':'2',
			'STARTED':'3',
			'SUCCESS':'4',
			'FAILURE':'5',
			'REVOKED':'6',
			'RETRY':'7'
			}

	def get_date(self, timestamp_str):

		return str(datetime.date.fromtimestamp(float(timestamp_str)))

	def __init__(self, dao_task, conn=None, flower=None):

		self.conn = conn
		self.flower = flower
		self._id = dao_task['id']
		self.uuid = dao_task['uuid']
		self.start_date = dao_task['start_date']
		self.end_date = dao_task['end_date']
		self.state = dao_task['state']
		self.state_updated_at = dao_task['state_updated_at']
		self.created_at = dao_task['created_at']
		self.updated_at = dao_task['updated_at']
		self.execution_id = dao_task['execution_id']

	def sync(self, trace_error=None):

		task = json.loads(urlopen(self.flower + '/api/tasks').read())[self.uuid]

		if task['exception'] is not None:
			trace_error.append('Task UUID: ' + self.uuid + '\n')
			trace_error.append(task['traceback'])

		if self.state != self.STATES[task['state']]:
			self.state = self.STATES[task['state']]
			if self.state != self.STATES['PENDING'] or self.state != self.STATE['RECEIVED']:
				self.start_date = self.get_date(task['started'])
			if self.state == self.STATES['SUCCESS']:
				self.end_date = self.get_date(task['succeeded'])
			elif self.state == self.STATES['FAILURE']:
				self.end_date = self.get_date(task['failed'])
			elif self.state == self.STATES['REVOKED']:
				self.end_date = self.get_date(task['revoked'])
			self.state_updated_at = str(datetime.datetime.now())
			self.updated_at = str(datetime.datetime.now())

	def save(self):

		self.updated_at = datetime.datetime.now()

		dao_task = DAOTask(self.conn)
		dao_task.update(self._id,
						self.start_date,
						self.end_date,
						self.state,
						self.state_updated_at,
						self.updated_at
						)
