from dao.Execution import Execution as DAOExecution
from entities.Execution import Execution

class Executions():

	executions = []

	def __init__(self, conn):
		self.conn = conn

	def load_enqueued_executing(self):
		dao_execution = DAOExecution(self.conn)
		for each_execution in dao_execution.get_enqueued_executing():
			execution = Execution(each_execution, conn=self.conn)
			self.executions.append(execution)
