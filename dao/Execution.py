from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

class Execution():

	def __init__(self, connection):
		self.conn = connection

	def get_enqueued_executing(self):
		cur = self.conn.cursor(cursor_factory=DictCursor)
		cur.execute('SELECT ' +
					'id, ' +
					'description, ' +
					'state, ' +
					'started_at, ' +
					'finished_at, ' +
					'trace_error, ' +
					'created_at, ' +
					'updated_at, ' +
					'executed_by_id, ' +
					'version_id ' +
					'results_available ' +
					'FROM execution_execution ' +
					'WHERE state = \'1\' or state = \'2\';'
					)
		rows = cur.fetchall()
		return rows

	def update(self, _id, state, started_at, finished_at, trace_error, updated_at, results_available):
		cur = self.conn.cursor(cursor_factory=DictCursor)
		query = ('UPDATE execution_execution SET ' +
				'state= \'' + str(state) + '\', ' +
				'started_at= \'' + str(started_at) + '\', ' +
				'finished_at= \'' + str(finished_at) + '\', ' +
				'trace_error= \'' + str(trace_error).replace('\'', '"') + '\', ' +
				'updated_at= \'' + str(updated_at) + '\' ' +
				'results_available= ' + str(results_available) + ' ' +
				'WHERE id=' + str(_id) + ';')
		query = query.replace('\'None\'', 'NULL')
		cur.execute(query)
		self.conn.commit()
		cur.close()

	def flush_trace_error(self, _id):
		cur = self.conn.cursor(cursor_factory=DictCursor)
		query = ('UPDATE execution_execution SET ' +
				'trace_error= \'\' ' +
				'WHERE id=' + str(_id) + ';')
		query = query.replace('\'None\'', 'NULL')
		cur.execute(query)
		self.conn.commit()
		cur.close()
