import pandas as pd
import datetime as dt
import yfinance as yf
import requests
import json


class Registro:
    """Class representing a financial record.

    This class represents a financial record with attributes such as
    fecha_compra, categoria, ticker, cantidad, and monto.

    Attributes:
        id_registro (int): An integer representing the ID of the record (initially set to None).
        fecha_compra (str): A string representing the purchase date.
        categoria (str): A string representing the category of the record.
        ticker (str): A string representing the ticker symbol.
        cantidad (str): A string representing the quantity.
        monto (float): A float representing the amount.

    Methods:
        __str__: Returns a string representation of the record.
    """

    def __init__(self, fecha_compra, categoria, ticker, cantidad, monto):
        """
        Initialize a financial record with given attributes.

        Parameters:
            fecha_compra (str): The purchase date.
            categoria (str): The category of the record.
            ticker (str): The ticker symbol.
            cantidad (str): The quantity.
            monto (float): The amount.
        """
        self.id_registro = None
        self.fecha_compra = fecha_compra
        self.categoria = categoria
        self.ticker = ticker
        self.cantidad = cantidad
        self.monto = monto

    def __str__(self):
        """
        Return a string representation of the record.

        Returns:
            str: A string representation of the record.
        """
        return f'''Registro[{self.fecha_compra}, {self.categoria},
    {self.ticker}, {self.cantidad}, {self.monto}]'''


def guardar(registro, conexion):
    """Save a financial record to the database.

    This function saves a given financial record to the database. The record's details are extracted
    based on the record's category and ticker symbol. The appropriate SQL statement is constructed
    based on the category and current market data, and then executed using the database connection.

    Args:
        registro (Registro): An instance of the Registro class representing the financial record to be saved.
        conexion: The database connection to execute the SQL statement.

    Returns:
        None

    Raises:
        None
    """
    tipo = registro.categoria[:1]

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------- FCIs ---------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    if tipo == "1":
        tables = pd.read_html(f"https://www.bullmarketbrokers.com/Information/FundData?ticker={registro.ticker}", decimal=',', thousands='.')

        valor_actual = tables[1][1][0]
        date_str = tables[1][1][1]
        date_object = dt.datetime.strptime(date_str, '%d/%m/%Y').date()

        sql = f"""INSERT INTO finance (fecha_compra, categoria, ticker, cantidad, monto, valor_actual, fecha_upd)
    VALUES('{registro.fecha_compra}', '{registro.categoria}', '{registro.ticker}', '{registro.cantidad}', {registro.monto}, {valor_actual}, '{date_object}')"""

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------- ACCIONES/CEDEARs --------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    if tipo == "2" or tipo == "3":
        data = yf.download(registro.ticker, period="5d", interval="1d")

        closing_price = data['Close'][0]
        date_object = data.index[0].to_pydatetime().date()

        sql = f"""INSERT INTO finance (fecha_compra, categoria, ticker, cantidad, monto, valor_actual, fecha_upd)
    VALUES('{registro.fecha_compra}', '{registro.categoria}', '{registro.ticker}', '{registro.cantidad}', {registro.monto}, {closing_price}, '{date_object}')"""

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------- USDs ---------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    if tipo == "4":
        url = "https://api.bluelytics.com.ar/v2/latest"
        res = requests.get(url)

        res = json.loads(res.content)
        valor_actual = res['blue']['value_buy']

        sql = f"""INSERT INTO finance (fecha_compra, categoria, ticker, cantidad, monto, valor_actual, fecha_upd)
    VALUES('{registro.fecha_compra}', '{registro.categoria}', '{registro.ticker}', '{registro.cantidad}', {registro.monto}, {valor_actual}, '{dt.date.today()}')"""

    else:
        pass

    try:
        print(f"'{registro.fecha_compra}', '{registro.categoria}', '{registro.ticker}', '{registro.cantidad}', {registro.monto}, {valor_actual}, '{dt.date.today()}'")
        conexion.cursor.execute(sql)
        conexion.close()

    except Exception as e:
        print(e.args)
        conexion.close()


def editar(registro, conexion, id_registro):
    """Edit a financial record in the database.

    This function updates a specific financial record in the 'finance' table of the database.
    The record is identified by the provided 'id_registro' parameter. The record's details are
    updated based on the attributes of the 'registro' object.

    Args:
        registro (Registro): An instance of the Registro class representing the updated financial record.
        conexion: The database connection to execute the SQL statement.
        id_registro (int): An integer representing the ID of the record to be edited.

    Returns:
        None

    Raises:
        None
    """
    sql = f"""UPDATE finance
    SET fecha_compra='{registro.fecha_compra}', categoria='{registro.categoria}', ticker='{registro.ticker}', cantidad='{registro.cantidad}', monto='{registro.monto}'
    WHERE id_registro={id_registro}"""

    try:
        conexion.cursor.execute(sql)
        conexion.close()
    except Exception as e:
        print(e.with_traceback)
        conexion.close()


def eliminar(id_registro, conexion):
    """Delete a financial record from the database.

    This function deletes a specific financial record from the 'finance' table of the database.
    The record to be deleted is identified by the provided 'id_registro' parameter.

    Args:
        id_registro (int): An integer representing the ID of the record to be deleted.
        conexion: The database connection to execute the SQL statement.

    Returns:
        None

    Raises:
        None
    """
    sql = f"""DELETE FROM finance
    WHERE id_registro={id_registro}"""

    try:
        conexion.cursor.execute(sql)
        conexion.close()
    except Exception as e:
        print(e.with_traceback)
        conexion.close()


def actualizar(conexion):
    """Update the current prices of financial records in the database.

    This function updates the current prices of financial records stored in the 'finance' table of the database.
    It retrieves the latest prices for different types of investments (FCIs, stocks/CEDEARs, USD) and updates
    the corresponding records in the database.

    Args:
        conexion: The database connection to execute the SQL statements.

    Returns:
        None

    Raises:
        None
    """
    url = "https://api.bluelytics.com.ar/v2/latest"
    res = requests.get(url)

    res = json.loads(res.content)
    valor_usd_actual = res['blue']['value_buy']

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------- FCIs ---------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    sql1 = 'SELECT id_registro, ticker, fecha_upd FROM finance WHERE substr(categoria, 1, 1)="1"'
    sql_jes = 'SELECT id_registro, ticker, fecha_upd FROM finance_jes WHERE substr(categoria, 1, 1)="1"'
    sql_mama = 'SELECT id_registro, ticker, fecha_upd FROM finance_mama WHERE substr(categoria, 1, 1)="1"'

    try:
        conexion.cursor.execute(sql1)
        lista_fcis = conexion.cursor.fetchall()

        conexion.cursor.execute(sql_jes)
        lista_fcis.extend(conexion.cursor.fetchall())

        conexion.cursor.execute(sql_mama)
        lista_fcis.extend(conexion.cursor.fetchall())

        for id_registro, ticker, fecha_upd in lista_fcis:
            tables = pd.read_html(f"https://www.bullmarketbrokers.com/Information/FundData?ticker={ticker}", decimal=',', thousands='.')

            date_str = tables[1][1][1]
            valor_actual = tables[1][1][0]
            date_object_fci = dt.datetime.strptime(date_str, '%d/%m/%Y').date()

            if str(date_object_fci) == str(fecha_upd):
                print("FCIs ya actualizados")
                break

            print(f"ID registro: {id_registro} FCI: {tables[0][1][1]}, valor actual: {valor_actual}, fecha: {date_str}")

            if (date_object_fci <= (dt.date.today() - dt.timedelta(days=1))):
                try:
                    conexion.cursor.execute(f"""UPDATE finance SET valor_actual={valor_actual}, fecha_upd='{date_object_fci}' WHERE id_registro={id_registro}""")
                    conexion.cursor.execute(f"""UPDATE finance_jes SET valor_actual={valor_actual}, fecha_upd='{date_object_fci}' WHERE id_registro={id_registro}""")
                    if id_registro == 125:
                        print(f"Entra a FCI usd,{valor_actual} * {valor_usd_actual}")
                        valor_actual = float(valor_actual)*float(valor_usd_actual)
                        conexion.cursor.execute(f"""UPDATE finance_mama SET valor_actual={valor_actual}, fecha_upd='{date_object_fci}' WHERE id_registro={id_registro}""")
                    conexion.cursor.execute(f"""UPDATE finance_mama SET valor_actual={valor_actual}, fecha_upd='{date_object_fci}' WHERE id_registro={id_registro}""")
                except Exception as e:
                    print("Error fci: ", e)

    except Exception as e:
        print("Error fci: ", e)
        conexion.cerrar()

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------- ACCIONES/CEDEARs --------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    sql2 = 'SELECT id_registro, ticker FROM finance WHERE substr(categoria, 1, 1)="2" or substr(categoria, 1, 1)="3"'

    try:
        conexion.cursor.execute(sql2)
        lista_acc = conexion.cursor.fetchall()

        for id_registro, ticker in lista_acc:

            data = yf.download(ticker, period="5d", interval="1d")

            closing_price = data['Close'][len(data) - 1]
            date_object = data.index[len(data) - 1].to_pydatetime().date()

            if (date_object <= dt.date.today()):
                try:
                    if dt.datetime.today().weekday() == 0:
                        try:
                            conexion.cursor.execute(f"""UPDATE finance SET valor_actual={closing_price:.2f}, fecha_upd='{dt.date.today() - dt.timedelta(days=3)}' WHERE id_registro={id_registro}""")
                        except Exception as e:
                            print("Error acc, cedear: ", e)
                    else:
                        if date_object_fci != dt.date.today() - dt.timedelta(days=1):
                            try:
                                conexion.cursor.execute(f"""UPDATE finance SET valor_actual={closing_price:.2f}, fecha_upd='{date_object_fci}' WHERE id_registro={id_registro}""")
                            except Exception as e:
                                print("Error acc, cedear: ", e)
                        else:
                            try:
                                conexion.cursor.execute(f"""UPDATE finance SET valor_actual={closing_price:.2f}, fecha_upd='{dt.date.today() - dt.timedelta(days=1)}' WHERE id_registro={id_registro}""")
                            except Exception as e:
                                print("Error acc, cedear: ", e)
                except Exception as e:
                    print(e)
                    conexion.cerrar()
    except Exception as e:
        print(e.with_traceback)
        conexion.cerrar()

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------- USDs ---------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    sql3 = 'SELECT id_registro, ticker FROM finance WHERE substr(categoria, 1, 1)="4"'

    try:
        conexion.cursor.execute(sql3)
        lista_usd = conexion.cursor.fetchall()
        url = "https://api.bluelytics.com.ar/v2/latest"
        res = requests.get(url)

        res = json.loads(res.content)
        valor_actual = res['blue']['value_buy']

        for id_registro, ticker in lista_usd:
            if dt.datetime.today().weekday() == 0:
                try:
                    conexion.cursor.execute(f"""UPDATE finance SET valor_actual={valor_actual}, fecha_upd='{dt.date.today()  - dt.timedelta(days=3)}' WHERE id_registro={id_registro}""")
                except Exception as e:
                    print("Error USD: ", e.with_traceback)
            else:
                if date_object_fci != dt.date.today() - dt.timedelta(days=1):
                    try:
                        conexion.cursor.execute(f"""UPDATE finance SET valor_actual={valor_actual}, fecha_upd='{date_object_fci}' WHERE id_registro={id_registro}""")
                    except Exception as e:
                        print("Error USD: ", e.with_traceback)
                        conexion.cerrar()
                else:
                    try:
                        conexion.cursor.execute(f"""UPDATE finance SET valor_actual={valor_actual}, fecha_upd='{dt.date.today()  - dt.timedelta(days=1)}' WHERE id_registro={id_registro}""")
                    except Exception as e:
                        print("Error USD: ", e.with_traceback)
                        conexion.cerrar()
    except Exception as e:
        print("Error fci: ", e.with_traceback)
        conexion.cerrar()


def appendear_historical(conexion):
    """Append updated financial records to the historical table.

    This function appends the updated financial records from the 'finance' table to the 'historical_finance_invertions'
    table in the database. It first creates the historical table if it doesn't exist. Then, it deletes the records from
    the historical table that have the latest update date and are present in the 'finance' table. Finally, it inserts
    the updated records from the 'finance' table into the historical table.

    Args:
        conexion: The database connection to execute the SQL statements.

    Returns:
        None

    Raises:
        None
    """

    sql1 = """CREATE TABLE IF NOT EXISTS historical_finance_invertions(
    id_registro INTEGER,
    fecha_compra TIMESTAMP,
    categoria VARCHAR(100),
    ticker VARCHAR(100),
    cantidad VARCHAR(100),
    monto FLOAT,
    valor_actual FLOAT,
    fecha_upd TIMESTAMP,
    PRIMARY KEY(id_registro)
    )"""

    try:
        conexion.cursor.execute(sql1)
    except Exception as e:
        print(e.with_traceback)
        conexion.cerrar()

    sql2 = '''DELETE FROM historical_finance_invertions
                WHERE fecha_upd = (
                SELECT MAX(fecha_upd)
                FROM historical_finance_invertions
                    WHERE id_registro IN (
                    SELECT id_registro
                    FROM finance
                        WHERE EXISTS (
                        SELECT 1
                        FROM historical_finance_invertions
                            WHERE id_registro = finance.id_registro AND fecha_upd >= finance.fecha_upd
                        )
                    )
                )'''

    sql3 = '''INSERT INTO historical_finance_invertions(id_registro, fecha_compra, categoria, ticker, cantidad, monto, valor_actual, fecha_upd)
            SELECT id_registro, fecha_compra, categoria, ticker, cantidad, monto, valor_actual, fecha_upd
            FROM finance
            WHERE NOT EXISTS (
                SELECT 1
                FROM historical_finance_invertions
                WHERE id_registro = finance.id_registro AND fecha_upd >= finance.fecha_upd
            )'''

    try:
        conexion.cursor.execute(sql2)
        conexion.cursor.execute(sql3)
    except Exception as e:
        print(e.with_traceback)
        conexion.cerrar()
