from dao.Execution import Execution as DAOExecution
from entities.Tasks import Tasks
import datetime

class Execution():

	STATES= {
			'ENQUEUED_STATE':'1',
			'EXECUTING_STATE':'2',
			'ERROR_STATE':'3',
			'COMPLETED_STATE':'4',
			'CANCELED_STATE':'5'
			}

	def load_tasks(self):

		self.tasks = Tasks(self.conn, self.flower)
		self.tasks.load_by_exec_id(self._id)

	def __init__(self, dao_execution, conn=None, flower=None):

		self.conn = conn
		self.flower = flower
		self._id = dao_execution['id']
		self.description = dao_execution['description']
		self.state = dao_execution['state']
		self.started_at = dao_execution['started_at']
		self.finished_at = dao_execution['finished_at']
		self.trace_error = dao_execution['trace_error']
		self.created_at = dao_execution['created_at']
		self.updated_at = dao_execution['updated_at']
		self.executed_by_id = dao_execution['executed_by_id']
		self.version_id = dao_execution['version_id']

	def sync(self):

		total_tasks = len(self.tasks.tasks)
		tasks_succeeded = 0
		tasks_failure = 0
		tasks_revoked = 0
		tasks_enqueued = 0
		tasks_started = 0
		trace_error = ''

		if total_tasks == 0:
			self.state = self.STATES['ERROR_STATE']
			self.trace_error = 'No tasks to execute'
		else:
			for each_task in self.tasks.tasks:
				if each_task.state == each_task.STATES['SUCCESS']:
					tasks_succeeded += 1
				elif each_task.state == each_task.STATES['FAILURE']:
					tasks_failure += 1
				elif each_task.state == each_task.STATES['REVOKED']:
					tasks_revoked += 1
				elif each_task.state == each_task.STATES['PENDING'] or each_task.state == each_task.STATES['RECEIVED']:
					tasks_enqueued += 1
				elif each_task.state == each_task.STATES['STARTED']:
					tasks_started += 1

			if tasks_started > 0:
				self.state = self.STATES['EXECUTING_STATE']
			elif tasks_enqueued == total_tasks:
				self.state = self.STATES['ENQUEUED_STATE']
			elif tasks_enqueued > 0:
				self.state = self.STATES['EXECUTING_STATE']
			elif tasks_revoked > 0:
				self.state = self.STATES['CANCELED_STATE']
			elif tasks_succeeded == total_tasks:
				self.state = self.STATES['COMPLETED_STATE']
			elif tasks_failure > 0:
				self.state = self.STATES['ERROR_STATE']

	def save(self):

		dao_execution = DAOExecution(self.conn)
		dao_execution.update(self._id,
							self.state,
							self.started_at,
							self.finished_at,
							self.trace_error,
							self.updated_at)
