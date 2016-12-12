from dao.Task import Task as DAOTask
import datetime

class Task():

	STATES= {
			'PENDING_STATE':'1',
			'RECEIVED_STATE':'2',
			'STARTED_STATE':'3',
			'SUCCESS_STATE':'4',
			'FAILURE_STATE':'5',
			'REVOKED_STATE':'6',
			'RETRY_STATE':'7'
			}

	def __init__(self, dao_task, conn=None):

		self.conn = conn
		self._id = dao_task['id']
		self.uuid = dao_task['uuid']
		self.start_date = dao_task['start_date']
		self.end_date = dao_task['end_date']
		self.state = dao_task['state']
		self.state_updated_at = dao_task['state_updated_at']
		self.created_at = dao_task['created_at']
		self.updated_at = dao_task['updated_at']
		self.execution_id = dao_task['execution_id']
