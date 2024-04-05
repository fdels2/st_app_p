class Registro_inf:
    """Class representing a financial record.

    This class represents a financial record with attributes such as
    mes and valor_ref.

    Attributes:
        id_registro: An integer representing the ID of the record (initially set to None).
        mes: An integer representing the date.
        valor_ref: A string representing the value reference of the record.

    Methods:
        __str__: Returns a string representation of the record.

    """
    def __init__(self, mes, valor_ref):
        """
        Initialize a financial record.

        Args:
            mes (int): The date of the record.
            valor_ref (str): The value reference of the record.
        """
        self.id_registro = None
        self.mes = mes
        self.valor_ref = valor_ref

    def __str__(self):
        """
        Return a string representation of the record.

        Returns:
            str: A string representation of the record.
        """
        return f'''Registro[{self.mes}, {self.valor_ref}]'''


def guardar(registro, conexion):
    """Save a financial record to the database.

    This function saves a given financial record to the database. The record's details are extracted
    based on the record's attributes 'mes' and 'valor_ref'. The appropriate SQL statement is constructed
    to insert these values into the 'inflation' table, and then executed using the provided database connection.

    Args:
        registro (Registro): An instance of the Registro class representing the financial record to be saved.
        conexion (object): The database connection object.

    Returns:
        None

    Raises:
        None
    """

    sql = f"""INSERT INTO inflation (mes, valor_ref)
    VALUES('{registro.mes}', '{registro.valor_ref}')"""

    try:
        print(f"'{registro.mes}', '{registro.valor_ref}'")
        conexion.cursor.execute(sql)

    except Exception as e:
        print(e.args)
        conexion.close()


def editar(registro, conexion, id_registro):
    """Edit a financial record in the database.

    This function updates a specific financial record in the 'inflation' table of the database.
    The record is identified by the provided 'id_registro' parameter. The record's details are
    updated based on the attributes of the 'registro' object.

    Args:
        registro (Registro): An instance of the Registro class representing the updated financial record.
        conexion (object): The database connection object.
        id_registro (int): An integer representing the ID of the record to be edited.

    Returns:
        None

    Raises:
        None
    """

    sql = f"""UPDATE inflation
    SET mes='{registro.mes}', valor_ref='{registro.valor_ref}'
    WHERE id_registro={id_registro}"""

    try:
        conexion.cursor.execute(sql)
    except Exception as e:
        print(e.with_traceback)
        conexion.close()


def eliminar(id_registro, conexion):
    """Delete a financial record from the database.

    This function deletes a specific financial record from the 'inflation' table of the database.
    The record to be deleted is identified by the provided 'id_registro' parameter.

    Args:
        id_registro (int): The ID of the record to be deleted.
        conexion (object): The database connection object.

    Returns:
        None

    Raises:
        None
    """

    sql = f"""DELETE FROM inflation
    WHERE id_registro={id_registro}"""

    try:
        conexion.cursor.execute(sql)
    except Exception as e:
        print(e.with_traceback)
        conexion.close()
