from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

class Task():

	def __init__(self, connection):
		self.conn = connection

	def get_by_exec_id(self, exec_id):
		cur = self.conn.cursor(cursor_factory=DictCursor)
		cur.execute('SELECT ' +
					'id, ' +
					'uuid, ' +
					'start_date, ' +
					'end_date, ' +
					'state, ' +
					'state_updated_at, ' +
					'created_at, ' +
					'updated_at, ' +
					'execution_id ' +
					'FROM execution_task ' +
					'WHERE execution_id = \'' + str(exec_id) + '\';')
		rows = cur.fetchall()
		return rows

	def update(self, _id, start_date, end_date, state, state_updated_at, updated_at):
		cur = self.conn.cursor(cursor_factory=DictCursor)
		query = ('UPDATE execution_task SET ' +
				'start_date=\'' + str(start_date) + '\', ' +
				'end_date=\'' + str(end_date) + '\', ' +
				'state=\'' + str(state) + '\', ' +
				'state_updated_at=\'' + str(state_updated_at) + '\', ' +
				'updated_at=\'' + str(updated_at) + '\' ' +
				'WHERE id=' + str(_id) + ';')

		query = query.replace('\'None\'', 'NULL')
		cur.execute(query)
		self.conn.commit()
		cur.close()
