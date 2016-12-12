from dao.Execution import Execution as DAOExecution
import datetime

class Execution():

	STATES= {
			'ENQUEUED_STATE ':'1',
			'EXECUTING_STATE ':'2',
			'ERROR_STATE ':'3',
			'COMPLETED_STATE ':'4',
			'CANCELED_STATE ':'5'
			}

	def __init__(self, dao_execution, conn=None):

		self.conn = conn
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
