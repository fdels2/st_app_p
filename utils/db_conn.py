import sqlite3
try:
    from df_def import execute_queries_df_last, execute_queries_df_hist, execute_queries_df_inf
except:
    from utils.df_def import execute_queries_df_last, execute_queries_df_hist, execute_queries_df_inf


class conexionDB:
    """Database Connection Class.

    This class represents a connection to the SQLite database used in the finance application.
    It initializes the connection to the database and provides a method to close the connection.

    Attributes:
        base_datos: A string representing the file path of the SQLite database.
        conexion: A SQLite connection object.
        cursor: A cursor object used to execute SQL queries.

    Methods:
        cerrar: Closes the database connection and commits any pending transactions.
    """
    def __init__(self):
        """Initialize the database connection."""
        self.base_datos = r'F:\Otros\Codigos importantes\Fede - mio\Finance_inverions\finance\database\finances_invertions.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        """Close the database connection."""
        self.conexion.commit()
        self.conexion.close()


def custom_query_resume(divider, table_suf):
    """Execute custom queries and retrieve summarized financial data.

    This function executes custom SQL queries on the historical and current financial data
    tables to retrieve summarized financial information. It calculates the quantity and amount
    by dividing the original values by the provided divider. The retrieved data is sorted by
    update date and record ID in descending order.

    Args:
        divider (int): A number to divide the quantity and amount for summarization.
        table_suf (str): A suffix to be appended to the table names for custom querying.

    Returns:
        DataFrame: A DataFrame containing summarized historical financial data.
        DataFrame: A DataFrame containing summarized current financial data.
    """
    sql_hist = f'''
        SELECT id_registro,
        fecha_compra,
        categoria,
        ticker,
        CAST(cantidad AS FLOAT) / {divider} AS cantidad,
        monto / {divider} AS monto,
        valor_actual,
        fecha_upd
        FROM historical_finance_invertions{table_suf}
        WHERE strftime('%Y-%m-%d', fecha_upd) > '2023-03-22'
        ORDER BY fecha_upd desc, id_registro desc
    '''
    sql_last = f'''
        SELECT id_registro,
        fecha_compra,
        categoria,
        ticker,
        CAST(cantidad AS FLOAT) / {divider} AS cantidad,
        monto / {divider} AS monto,
        valor_actual,
        fecha_upd
        FROM finance{table_suf}
        ORDER BY fecha_upd desc, id_registro desc
    '''

    conexion = conexionDB().conexion

    df_last = execute_queries_df_last(sql_last=sql_last, conexion=conexion)
    df_hist = execute_queries_df_hist(sql_hist=sql_hist, conexion=conexion)

    conexion.close()

    return df_hist, df_last


def custom_query_inf():
    """Execute a custom query to retrieve inflation data.

    This function executes a custom SQL query to retrieve inflation data from the 'inflation'
    table in the database. The retrieved data includes record ID, month, and inflation value,
    sorted by month and record ID in descending order.

    Returns:
        DataFrame: A DataFrame containing inflation data.
    """
    sql_inf = '''
        SELECT id_registro,
        mes,
        valor_ref
        FROM inflation
        ORDER BY mes desc, id_registro desc
    '''

    conexion = conexionDB().conexion

    df_inf = execute_queries_df_inf(sql=sql_inf, conexion=conexion)

    conexion.close()

    return df_inf
