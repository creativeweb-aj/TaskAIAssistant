from typing import List
from langchain.tools import Tool
import psycopg2
from pydantic.v1 import BaseModel

# Establish a connection to the database
conn = psycopg2.connect(dbname='task_management_db', user='postgres', password='12345', host='localhost')


def list_tables():
    # Create a cursor object
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    # Fetch the results
    rows = cur.fetchall()
    tables = []
    for row in rows:
        if row:
            tables.append(row[0])
    # Close the cursor and the connection
    cur.close()
    return tables


def run_postgresql_query(query):
    # Create a cursor object
    cur = conn.cursor()
    try:
        cur.execute(query)
        if query.lower().startswith('insert'):
            conn.commit()
            return "Query executed."
        else:
            # Fetch the results
            rows = cur.fetchall()
            # Close the cursor
            cur.close()
            return rows
    except Exception as err:
        # Close the cursor and the connection
        cur.close()
        if conn:
            conn.rollback()  # This is crucial to handle the error properly and continue with new commands
        return f"The following error occurred: {str(err)}"


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_postgresql_query",
    description="Run a postgresql query.",
    func=run_postgresql_query,
    args_schema=RunQueryArgsSchema
)


def describe_tables(table_names):
    print(f"table_names --> {table_names}")
    # Convert list items into a comma-separated string, with each item enclosed in single quotes
    tables = ", ".join(f"'{name}'" for name in table_names)
    print(f"tables --> {tables}")
    # Create a cursor object
    cur = conn.cursor()
    cur.execute(
        f"SELECT table_name, column_name FROM information_schema.columns "
        f"WHERE table_name IN ({tables});"
    )
    # Fetch the results
    rows = cur.fetchall()
    print(f'describe_tables --> {rows}, {type(rows)}')
    # Close the cursor and the connection
    cur.close()
    return rows


class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, column names, and data type information.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)
