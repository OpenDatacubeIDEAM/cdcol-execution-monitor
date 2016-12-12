from dao.Execution import Execution as DAOExecution
from entities.Execution import Execution

class Executions():

	def __init__(self, conn, flower):
		self.conn = conn
		self.flower = flower
		self.executions = []

	def load_enqueued_executing(self):
		dao_execution = DAOExecution(self.conn)
		for each_execution in dao_execution.get_enqueued_executing():
			execution = Execution(each_execution, conn=self.conn, flower=self.flower)
			execution.load_tasks()
			execution.sync()
			execution.save()
			self.executions.append(execution)
