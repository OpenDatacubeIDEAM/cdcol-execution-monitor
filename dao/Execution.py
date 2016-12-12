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
					'FROM execution_execution ' +
					'WHERE state = \'1\' or state = \'2\';'
					)
		rows = cur.fetchall()
		return rows
