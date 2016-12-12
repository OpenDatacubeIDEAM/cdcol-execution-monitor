from dao.Task import Task as DAOTask
from entities.Task import Task

class Tasks():

	def __init__(self, conn, flower):
		self.conn = conn
		self.flower = flower
		self.tasks = []

	def load_by_exec_id(self, exec_id):
		dao_task = DAOTask(self.conn)
		for each_task in dao_task.get_by_exec_id(exec_id):
			task = Task(each_task, conn=self.conn, flower=self.flower)
			task.sync()
			self.tasks.append(task)
