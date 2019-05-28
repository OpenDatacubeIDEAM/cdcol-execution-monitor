# CDCOL UPDATER

Update the state of executions of the WEB component using the states of the running Arclow dags.

1. Retrieve the executions which state is 'EN ESPERA' (1) from the Web database.
2. Retrieve the dag runs for a given execution.dag_id from the airflow database.
3. Updates the executions that have dag runs with state success or failed.

## Setting UP

Edit the following parameters to get it working properly.

```python
"""
Database connection data.
"""
AIRFLOW_DB_CONN_DATA = {
    'host':'172.24.99.218',
    'dbname':'airflow',
    'user':'airflow',
    'passwd':'cubocubo'
}

WEB_DB_CONN_DATA = {
    'host':'172.24.99.218',
    'dbname':'ideam',
    'user':'portal_web',
    'passwd':'CDCol_web_2016'
}
```

Place the file **cdcol_updater_dag.py** in /web_storage/dags. 


```sh
cp cdcol_updater_dag.py /web_storage/dags/
```

Place the **cdcol_updater** folder into the algorithms folder.

```sh
cp -R cdcol_updater /web_storage/algorithms/
```
