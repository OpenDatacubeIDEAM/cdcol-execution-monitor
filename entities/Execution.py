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
		self.tasks.load_by_exec_id(self._id, self.TRACE_ERROR)

	def __init__(self, dao_execution, conn=None, flower=None):

		self.conn = conn
		self.TRACE_ERROR = []
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
		start_time = None
		end_time = None

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

				task_start = each_task.start_date
				task_end = each_task.end_date

				if start_time is None:
					start_time = task_start
				elif task_start < start_time:
					start_time = task_start

				if end_time is None:
					end_time = task_end
				elif task_end > end_time:
					end_time = task_end

			if tasks_started > 0:
				self.state = self.STATES['EXECUTING_STATE']
			elif tasks_enqueued == total_tasks:
				self.state = self.STATES['ENQUEUED_STATE']
			elif tasks_enqueued > 0:
				self.state = self.STATES['EXECUTING_STATE']
			elif tasks_revoked > 0:
				self.state = self.STATES['CANCELED_STATE']
				self.finished_at = end_time
			elif tasks_succeeded == total_tasks:
				self.state = self.STATES['COMPLETED_STATE']
				self.finished_at = end_time
			elif tasks_failure > 0:
				self.state = self.STATES['ERROR_STATE']
				self.finished_at = end_time

		for each_trace in self.TRACE_ERROR:
			self.trace_error += str(each_trace)

	def save(self):

		self.updated_at = datetime.datetime.now()

		dao_execution = DAOExecution(self.conn)
		dao_execution.update(self._id,
							self.state,
							self.started_at,
							self.finished_at,
							self.trace_error,
							self.updated_at)

	def flush_trace_error(self):

		dao_execution = DAOExecution(self.conn)
		dao_execution.flush_trace_error(self._id)
		self.trace_error = ''
