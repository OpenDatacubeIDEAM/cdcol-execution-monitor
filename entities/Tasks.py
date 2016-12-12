from dao.Task import Task as DAOTask
from entities.Task import Task

class Tasks():

	def __init__(self, conn):
		self.conn = conn
		self.tasks = []

	def load_by_exec_id(self, exec_id):
		dao_task = DAOTask(self.conn)
		for each_task in dao_task.get_by_exec_id(exec_id):
			task = Task(each_task, conn=self.conn)
			self.tasks.append(task)
