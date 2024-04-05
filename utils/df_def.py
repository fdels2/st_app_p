import pandas as pd


def execute_queries_df_inf(sql, conexion):
    """
    Execute SQL query and return the result as a pandas DataFrame.

    Parameters:
    - sql (str): The SQL query to be executed.
    - conexion: The connection object to the database.

    Returns:
    pandas.DataFrame: A DataFrame containing the result of the SQL query.

    Note:
    This function is designed specifically for executing SQL queries related to inflation data.
    """
    return pd.read_sql_query(sql, conexion)


def execute_queries_df_last(sql_last, conexion):
    """
    Execute SQL query to fetch the last data entries and perform calculations on the DataFrame.

    Parameters:
    - sql_last (str): The SQL query to fetch the last data entries.
    - conexion: The connection object to the database.

    Returns:
    pandas.DataFrame: A DataFrame containing the last data entries with additional calculated columns.

    Notes:
    - This function assumes that the SQL query retrieves the last entries from a database table.
    - It calculates 'monto_actual' by multiplying 'valor_actual' with 'cantidad'.
    - It calculates 'diferencia' by subtracting 'monto_actual' from 'monto'.
    - It calculates 'gan%' by dividing 'diferencia' by 'monto' and multiplying by 100.
    """
    df_last = pd.read_sql_query(sql_last, conexion)
    df_last['monto_actual'] = df_last['valor_actual'] * df_last['cantidad']
    df_last['diferencia'] = df_last['monto_actual'] - df_last['monto']
    df_last['gan%'] = df_last['diferencia'] / df_last['monto'] * 100
    return df_last


def execute_queries_df_hist(sql_hist, conexion):
    """
    Execute SQL query to fetch historical data and perform calculations on the DataFrame.

    Parameters:
    - sql_hist (str): The SQL query to fetch historical data.
    - conexion: The connection object to the database.

    Returns:
    pandas.DataFrame: A DataFrame containing the historical data with additional calculated columns.

    Notes:
    - This function assumes that the SQL query retrieves historical data from a database table.
    - It calculates 'monto_actual' by multiplying 'valor_actual' with 'cantidad'.
    - It calculates 'diferencia' by subtracting 'monto_actual' from 'monto'.
    - It calculates 'gan%' by dividing 'diferencia' by 'monto' and multiplying by 100.
    """
    df_hist = pd.read_sql_query(sql_hist, conexion)
    df_hist['monto_actual'] = df_hist['valor_actual'] * df_hist['cantidad']
    df_hist['diferencia'] = df_hist['monto_actual'] - df_hist['monto']
    df_hist['gan%'] = df_hist['diferencia'] / df_hist['monto'] * 100
    return df_hist


def last_usd_total(df_last):
    """
    Calculate the total USD amount grouped by category from the last DataFrame.

    Parameters:
    - df_last (pandas.DataFrame): DataFrame containing the last data entries.

    Returns:
    pandas.DataFrame: A DataFrame containing the total USD amount grouped by category.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'categoria' and 'cantidad'.
    - It groups the data by 'categoria' and calculates the sum of 'cantidad'.
    - It filters the result to include only categories containing "USD".
    """
    df_last_usd_total = df_last.groupby(['categoria']).agg({'cantidad': 'sum'}).round().reset_index()
    df_last_usd_total = df_last_usd_total[df_last_usd_total['categoria'].str.contains("USD")]
    return df_last_usd_total


def hist_day_summary(df_hist):
    """
    Summarize historical data grouped by update date.

    Parameters:
    - df_hist (pandas.DataFrame): DataFrame containing historical data.

    Returns:
    pandas.DataFrame: A DataFrame summarizing historical data, grouped by update date,
    with the sum of 'monto' and 'monto_actual' for each date.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'fecha_upd', 'monto', and 'monto_actual'.
    - It groups the data by 'fecha_upd' and calculates the sum of 'monto' and 'monto_actual'.
    """
    return df_hist.groupby(['fecha_upd']).agg({'monto': 'sum', 'monto_actual': 'sum'}).reset_index()


def last_cat_summary(df_last):
    """
    Summarize data from the last DataFrame grouped by category.

    Parameters:
    - df_last (pandas.DataFrame): DataFrame containing the last data entries.

    Returns:
    pandas.DataFrame: A DataFrame summarizing data grouped by category,
    with the sum of 'monto', 'monto_actual', and 'diferencia' for each category.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'categoria', 'monto', 'monto_actual', and 'diferencia'.
    - It groups the data by 'categoria' and calculates the sum of 'monto', 'monto_actual', and 'diferencia'.
    """
    return df_last.groupby(['categoria']).agg({'monto': 'sum', 'monto_actual': 'sum', 'diferencia': 'sum'}).round().reset_index()


def last_cat_ev_summ(df_last, df_hist):
    """
    Summarize the evolution of data from the last DataFrame grouped by category.

    Parameters:
    - df_last (pandas.DataFrame): DataFrame containing the last data entries.
    - df_hist (pandas.DataFrame): DataFrame containing historical data.

    Returns:
    pandas.DataFrame: A DataFrame summarizing the evolution of data grouped by category,
    including the total 'monto', 'monto_actual', 'evolucion_invertido', 'evolucion_actual',
    'porcentaje_diferencia', 'diferencia_portafolio', and 'porcentaje_dif_portafolio'.

    Notes:
    - This function assumes that the input DataFrames contain columns including 'categoria', 'monto', 'monto_actual', and 'diferencia'.
    - It calculates the evolution of 'monto' and 'monto_actual' using historical data.
    - It calculates the percentage difference between current and previous evolutions.
    - It calculates the total 'diferencia' and its percentage of the total 'monto'.
    """
    df_hist_day_summ = hist_day_summary(df_hist)
    df_last_cat_summ = last_cat_summary(df_last=df_last)

    df_last_cat_ev_summ = pd.DataFrame({'categoria': ['Total'],
                                        'monto': df_last_cat_summ['monto'].sum().round(),
                                        'evolucion_invertido': [df_hist_day_summ['monto'].round().tolist()],
                                        'monto_actual': df_last_cat_summ['monto_actual'].sum().round(),
                                        'evolucion_actual': [df_hist_day_summ['monto_actual'].round().tolist()]
                                        })
    df_last_cat_ev_summ['porcentaje_diferencia'] = (((df_last_cat_ev_summ['evolucion_actual'].apply(lambda x: x[-1]) - df_last_cat_ev_summ['evolucion_actual'].apply(lambda x: x[-2])) / df_last_cat_ev_summ['evolucion_actual'].apply(lambda x: x[-2])) * 100).round(2)
    df_last_cat_ev_summ['diferencia_portafolio'] = df_last_cat_summ['diferencia'].sum().round()
    df_last_cat_ev_summ['porcentaje_dif_portafolio'] = ((df_last_cat_summ['diferencia'].sum().round() / df_last_cat_summ['monto'].sum().round())*100)
    return df_last_cat_ev_summ


def hist_day_cat_summary(df_hist):
    """
    Summarize historical data grouped by update date and category.

    Parameters:
    - df_hist (pandas.DataFrame): DataFrame containing historical data.

    Returns:
    pandas.DataFrame: A DataFrame summarizing historical data grouped by update date and category,
    with the sum of 'monto' and 'monto_actual' for each category and date.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'categoria', 'fecha_upd', 'monto', and 'monto_actual'.
    - It groups the data by 'categoria' and 'fecha_upd', and calculates the sum of 'monto' and 'monto_actual'.
    - It renames the columns to match the desired output format.
    """
    df_hist_day_cat_summ = df_hist.groupby(['categoria', 'fecha_upd']).agg({'monto': 'sum', 'monto_actual': 'sum'}).reset_index()
    df_hist_day_cat_summ.columns = ['categoria', 'fecha_upd', 'monto_actual', 'monto']
    return df_hist_day_cat_summ


def last_cat_ev_summ_cat(df_last, df_hist):
    """
    Summarize the evolution of data from the last DataFrame grouped by category and update date.

    Parameters:
    - df_last (pandas.DataFrame): DataFrame containing the last data entries.
    - df_hist (pandas.DataFrame): DataFrame containing historical data.

    Returns:
    pandas.DataFrame: A DataFrame summarizing the evolution of data grouped by category,
    including the total 'monto_actual', 'monto', 'porcentaje_diferencia', 'diferencia_portafolio',
    and 'porcentaje_dif_portafolio'.

    Notes:
    - This function assumes that the input DataFrames contain columns including 'categoria', 'fecha_upd', 'monto', 'monto_actual', and 'diferencia'.
    - It calculates the evolution of 'monto' and 'monto_actual' using historical data.
    - It calculates the percentage difference between current and previous evolutions.
    - It calculates the total 'diferencia' and its percentage of the total 'monto_actual'.
    """
    df_hist_day_cat_summ = hist_day_cat_summary(df_hist)

    df_last_cat_ev_summ_cat = df_hist_day_cat_summ.groupby('categoria').agg(
        monto_actual_sum_last=('monto_actual', 'last'),
        monto_actual_lista=('monto_actual', list),
        monto_sum_last=('monto', 'last'),
        monto_sum_lista=('monto', list)
    ).reset_index()
    df_last_cat_ev_summ_cat['porcentaje_diferencia'] = (
        ((df_last_cat_ev_summ_cat['monto_sum_lista'].apply(lambda x: x[-1]) - df_last_cat_ev_summ_cat['monto_sum_lista'].apply(lambda x: x[-2])) / df_last_cat_ev_summ_cat['monto_sum_lista'].apply(lambda x: x[-2])) * 100).round(2).apply(lambda x: f'{x:.2f}% {"🔴" if x < 0 else "🟢"}')
    df_diferencia_portafolio = df_last.groupby(['categoria']).agg({'diferencia': 'sum'}).round().reset_index()

    df_last_cat_ev_summ_cat = pd.merge(
        df_last_cat_ev_summ_cat,
        df_diferencia_portafolio,
        on='categoria',
        how='left',
        suffixes=('_cat_ev_summ', '_diferencia_portafolio')
    )
    df_last_cat_ev_summ_cat['porcentaje_dif_portafolio'] = ((df_last_cat_ev_summ_cat['diferencia'].round() / df_last_cat_ev_summ_cat['monto_actual_sum_last'].round())*100)
    df_last_cat_ev_summ_cat.rename(columns={'diferencia': 'diferencia_portafolio'}, inplace=True)
    return df_last_cat_ev_summ_cat


def agrupado_ticker_resumen(df_hist):
    """
    Summarize data grouped by ticker and update date, focusing on the evolution of 'valor_actual'.

    Parameters:
    - df_hist (pandas.DataFrame): DataFrame containing historical data.

    Returns:
    pandas.DataFrame: A DataFrame summarizing data grouped by ticker,
    including the last 'valor_actual', 'categoria', and 'porcentaje_diferencia'.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'ticker', 'fecha_upd', 'valor_actual', and 'categoria'.
    - It calculates the evolution of 'valor_actual' for each ticker using historical data.
    - It calculates the percentage difference between the current and previous values of 'valor_actual'.
    """
    df_agrupado_ticker = df_hist.groupby(['ticker', 'fecha_upd']).agg({'valor_actual': 'last', 'categoria': 'last'}).reset_index()
    df_agrupado_ticker.columns = ['ticker', 'fecha_upd', 'valor_actual_last', 'categoria']

    df_agrupado_ticker_resumen = df_agrupado_ticker.groupby('ticker').agg(
        valor_actual_last=('valor_actual_last', 'last'),
        categoria=('categoria', 'last'),
        valor_actual_last_lista=('valor_actual_last', list)
    ).reset_index()
    df_agrupado_ticker_resumen['porcentaje_diferencia'] = (((df_agrupado_ticker_resumen['valor_actual_last_lista'].apply(lambda x: x[-1]) - df_agrupado_ticker_resumen['valor_actual_last_lista'].apply(lambda x: x[-2])) / df_agrupado_ticker_resumen['valor_actual_last_lista'].apply(lambda x: x[-2])) * 100).round(2)
    return df_agrupado_ticker_resumen


def last_ticker_summ(df_last):
    """
    Summarize data from the last DataFrame grouped by ticker.

    Parameters:
    - df_last (pandas.DataFrame): DataFrame containing the last data entries.

    Returns:
    pandas.DataFrame: A DataFrame summarizing data grouped by ticker,
    including the last 'categoria', and the sum of 'monto', 'monto_actual', and 'diferencia'.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'ticker', 'categoria', 'monto', 'monto_actual', and 'diferencia'.
    - It groups the data by 'ticker' and calculates the last 'categoria', and the sum of 'monto', 'monto_actual', and 'diferencia'.
    """
    return df_last.groupby(['ticker']).agg({'categoria': 'last', 'monto': 'sum', 'monto_actual': 'sum', 'diferencia': 'sum'}).round().reset_index()


def inf_mensual(df):
    """
    Calculate monthly inflation rate based on the DataFrame.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing inflation data.

    Returns:
    pandas.DataFrame: A DataFrame with monthly inflation rates calculated.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'mes' (month), and 'valor_ref' (reference value for inflation).
    - It sorts the DataFrame by 'mes' in ascending order.
    - It converts the 'mes' column to datetime format.
    - It calculates the monthly inflation rate ('ipc_mensual') as the percentage change of 'valor_ref' rounded to 2 decimal places.
    """
    df_inf_order = df.sort_values(by='mes', ascending=True).reset_index(drop=True)
    df_inf_order['mes'] = pd.to_datetime(df_inf_order['mes'])
    df_inf_order['ipc_mensual'] = (df_inf_order['valor_ref'].pct_change() * 100).round(2)

    return df_inf_order


def inf_interanual(df):
    """
    Calculate year-over-year inflation rate based on the DataFrame.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing inflation data.

    Returns:
    pandas.DataFrame: A DataFrame with year-over-year inflation rates calculated.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'mes' (month), and 'valor_ref' (reference value for inflation).
    - It shifts the DataFrame by 12 months to align with the same period of the previous year.
    - It merges the shifted DataFrame with the original DataFrame based on the index.
    - It calculates the year-over-year inflation rate ('ipc_interanual') as the percentage change between the current and previous year's reference values.
    - It drops unnecessary columns and renames the remaining columns to match the desired output format.
    """
    df_shift12 = df.iloc[12:].reset_index(drop=True)
    df_merged = df_shift12.merge(df, left_index=True, right_index=True)

    df_merged['ipc_interanual'] = (((df_merged['valor_ref_x'] - df_merged['valor_ref_y']) / df_merged['valor_ref_y']) * 100).round(2)
    df_merged = df_merged.drop(['mes_y', 'id_registro_x', 'id_registro_y', 'valor_ref_y', 'ipc_mensual_y'], axis=1)
    df_merged.rename(columns={'mes_x': 'mes', 'ipc_mensual_x': 'ipc_mensual', 'valor_ref_x': 'valor_ref'}, inplace=True)
    return df_merged


def inf_acumulado(df):
    """
    Calculate cumulative inflation based on the DataFrame.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing inflation data.

    Returns:
    pandas.DataFrame: A DataFrame with cumulative inflation rates calculated.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'mes' (month), and 'valor_ref' (reference value for inflation).
    - It converts the 'mes' column to datetime format.
    - It creates a new column 'mes_aux' by adding one year to each month to find the corresponding December of the next year.
    - It filters the DataFrame to keep only rows where the month is December.
    - It merges the original DataFrame with the filtered DataFrame based on the year of each month.
    - It calculates the cumulative inflation ('ipc_acum') as the percentage change between the reference values of consecutive Decembers.
    - It drops unnecessary columns and renames the remaining columns to match the desired output format.
    """
    df['mes'] = pd.to_datetime(df['mes'])
    df['mes_aux'] = df['mes'] + pd.offsets.DateOffset(years=1)

    # Filtrar las filas donde el mes sea diciembre
    df_diciembre = df[df['mes_aux'].dt.month == 12]

    df_merged = df.merge(df_diciembre, how="left", left_on=df['mes'].dt.year, right_on=df_diciembre['mes_aux'].dt.year)
    df_merged['ipc_acum'] = (((df_merged['valor_ref_x'] - df_merged['valor_ref_y']) / df_merged['valor_ref_y']) * 100).round(2)
    df_merged = df_merged.drop(['key_0', 'valor_ref_x', 'valor_ref_y', 'mes_y', 'mes_aux_y', 'mes_aux_x', 'ipc_mensual_y', 'ipc_interanual_y'], axis=1)
    df_merged.rename(columns={'mes_x': 'mes', 'ipc_mensual_x': 'ipc_mensual', 'ipc_interanual_x': 'ipc_interanual'}, inplace=True)
    return df_merged
