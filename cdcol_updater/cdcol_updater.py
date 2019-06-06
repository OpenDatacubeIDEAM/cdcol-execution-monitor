# -*- coding: utf-8 -*-

"""
    cdcol_updater 

    1. Retrieve the executions which state is 'EN ESPERA' (1).
        from the Web database.
    2. Retrieve the dag runs for a given execution.dag_id 
        from the airflow database.
    3. Updates the executions that have dag runs with state 
        success or failed.
"""

import psycopg2
import logging
import os


logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)


"""
Database connection data.
"""
AIRFLOW_DB_CONN_DATA = {
    'host':'192.168.106.21',
    'dbname':'airflow',
    'user':'airflow',
    'passwd':'cubocubo'
}

WEB_DB_CONN_DATA = {
    'host':'192.168.106.21',
    'dbname':'ideam_1',
    'user':'portal_web',
    'passwd':'CDCol_web_2016'
}



WEB_EXECUTING_STATE = '2'
WEB_ERROR_STATE = '3'
WEB_COMPLETED_STATE = '4'

AIRFLOW_TO_WEB_STATES = {
    'running': WEB_EXECUTING_STATE,
    'success': WEB_COMPLETED_STATE,
    'failed': WEB_ERROR_STATE
}


def select_query(query_str,conn_data):
    """Perform select queries.
    
    Args:
        query_str (str): SQL query to be performed.
        conn_data (dict): a dictionary with database conection 
            data.
    """
    connection_format = (
        "dbname='%(dbname)s' " 
        "user='%(user)s' "
        "host='%(host)s' "
        "password='%(passwd)s'"
    )

    connection_str = connection_format % conn_data

    # Opening connecting
    connection = psycopg2.connect(connection_str)
    cursor = connection.cursor()

    # Performing query
    cursor.execute(query_str)
    rows = cursor.fetchall()

    # Close connection
    connection.close()

    return rows


def update_query(query_str,conn_data):
    """Perform update queries.
    
    Args:
        query_str (str): SQL query to be performed.
        conn_data (dict): a dictionary with database conection 
            data. 
    """
    connection_format = (
        "dbname='%(dbname)s' " 
        "user='%(user)s' "
        "host='%(host)s' "
        "password='%(passwd)s'"
    )

    connection_str = connection_format % conn_data

    # Opening connecting
    connection = psycopg2.connect(connection_str)
    cursor = connection.cursor()

    # Performing query
    cursor.execute(query_str)
    connection.commit()

    # updated row count
    row_count = cursor.rowcount
   
    # Close connection
    connection.close()

    return row_count


def get_enqueued_state_executions():
    """Return the executions in state "EN ESPERA"
    
    Retrieve the executions form execution_execution
    which has state == 1
    """

    query_format = (
        'SELECT '
        'dag_id '
        'FROM execution_execution '
        'WHERE state = \'%s\' OR state = \'%s\';'
    )

    query_str = query_format % ('1','2')
    rows = select_query(query_str,WEB_DB_CONN_DATA)
    return rows


def get_dag_run(dag_id):
    """Return the executions in state "EN ESPERA"
    
    Retrieve the executions from execution_execution
    which has state == 1
    """

    query_format = (
        'SELECT '
        'dag_id, '
        'state, '
        'start_date, '
        'end_date, '
        'execution_date '
        'FROM dag_run '
        'WHERE dag_id = \'%s\' ;'
    )

    query_str = query_format % (dag_id,)
    rows = select_query(query_str,AIRFLOW_DB_CONN_DATA)

    return rows[-1] if rows else None


def update_execution(**fields):
    """Update the execution_execution table form the web database.

    Updates the state, started_at, finished_at and 
    results_available fields of a given dag_id
    """

    query_format_1 = (
        'UPDATE execution_execution SET '
        'state=\'%(state)s\', '
        'started_at=\'%(start_date)s\', '
        'finished_at=\'%(end_date)s\', '
        'results_available=TRUE '
        'WHERE dag_id=\'%(dag_id)s\';'
    )



    query_format_2 = (
        'UPDATE execution_execution SET '
        'state=\'%(state)s\', '
        'started_at=\'%(start_date)s\' '
        'WHERE dag_id=\'%(dag_id)s\';'
    )

    end_date = fields.get('end_date')

    query_format = query_format_1 if end_date else query_format_2
    query_str = query_format % fields
    row_count = update_query(query_str,WEB_DB_CONN_DATA)
    return row_count


def update_executions():
    """Update Success or Failed executions.

    1. Retrieve the executions which state is 'EN ESPERA' (1).
        from the Web database.
    2. Retrieve the dag runs for a given execution.dag_id 
        from the airflow database.
    3. Updates the executions that have dag runs with state 
        success or failed
    """
    executions = get_enqueued_state_executions()
    for dag_id, in executions:
        dag_run = get_dag_run(dag_id)
        logging.info(
            'Checking Dag %s, has runs (%s)',
            dag_id,
            bool(dag_run)
        )
        if dag_run:
            dag_id, dag_state, start_date, end_date, execution_date = dag_run
            logging.info(
                'Dag %s has finished (%s), state (%s)',dag_id,bool(end_date),dag_state
            )

            state = AIRFLOW_TO_WEB_STATES.get(dag_state)
            updated = update_execution(
                dag_id=dag_id,
                state=state,
                start_date=start_date,
                end_date=end_date,
                execution_date=execution_date,
            )
            logging.info('Dag %s updated (%s)',dag_id,bool(updated))
            


if __name__ == '__main__':
    update_executions()
