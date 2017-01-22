from dao.Execution import Execution as DAOExecution
from entities.Execution import Execution

class Executions():

	def __init__(self, conn, flower, results_path, make_mosaic_script):
		self.conn = conn
		self.flower = flower
		self.executions = []
		self.results_path = results_path
		self.make_mosaic_script = make_mosaic_script

	def load_enqueued_executing(self):
		dao_execution = DAOExecution(self.conn)
		for each_execution in dao_execution.get_enqueued_executing():
			execution = Execution(each_execution, conn=self.conn, flower=self.flower, results_path=self.results_path, make_mosaic_script=self.make_mosaic_script)
			execution.flush_trace_error()
			execution.load_tasks()
			execution.sync()
			execution.save()
			self.executions.append(execution)
