from utils.db_conn import conexionDB, custom_query_resume
from utils.st_def import st
from utils.functions import guardar, editar, eliminar, Registro
import time
from datetime import datetime


#  page config
st.set_page_config(page_title="Finance inv", page_icon=":memo:", layout="wide", initial_sidebar_state="collapsed")

#  sidebar config
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 50px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# sidebar parameters
st.sidebar.header('Parametros')
value = 10 if st.sidebar.toggle('//') else 1
table_suf = "_jes" if st.sidebar.toggle('Jes') else ("_mama" if st.sidebar.toggle('Mama') else "")
df_hist, df_last = custom_query_resume(divider=value, table_suf=table_suf)

# page config
col1, col2 = st.columns([4, 1])
with col1:
    st.header("""Gestión de registros""",
              divider='red')
with col2:
    st.header(f"""*:grey[{datetime.now().date()}]*""")


def dataframe_with_selections(df):
    """
    Enable user selection of rows in a DataFrame using Streamlit's data editor.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing the data to be displayed and selected by the user.

    Returns:
    pandas.DataFrame or None: A DataFrame containing the row selected by the user, or None if no row is selected.

    Notes:
    - This function assumes that the input DataFrame contains columns including 'id_registro', 'fecha_compra', 'categoria', 'ticker', 'cantidad', 'monto', 'valor_actual', 'fecha_upd', 'monto_actual', 'diferencia', and 'gan%'.
    - It adds a new column 'Select' to the DataFrame with all values initially set to False.
    - It displays the DataFrame with checkboxes for row selection using Streamlit's data editor.
    - It allows the user to select only one row.
    - It returns the selected row as a DataFrame after removing the 'Select' column, if a row is selected.
    - If no row is selected, it returns None and displays a message.
    - If more than one row is selected, it displays a warning message and returns None.
    """
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        height=(df_last.shape[0] + 1) * 35 + 3,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=True),
            "id_registro": st.column_config.Column("Id", width="small"),
            "fecha_compra": st.column_config.Column("F. compra", width="small"),
            "categoria": st.column_config.Column("Categoria", width="small"),
            "ticker": st.column_config.Column("Ticker", width="small"),
            "cantidad": st.column_config.Column("Cantidad", width="small"),
            "monto": st.column_config.NumberColumn("Invertido", width="small", format="$ %d"),
            "valor_actual": st.column_config.NumberColumn("V. actual", width="small", format="$ %d"),
            "fecha_upd": st.column_config.Column("F. upd", width="small"),
            "monto_actual": st.column_config.NumberColumn("M. actual", width="small", format="$ %d"),
            "diferencia": st.column_config.NumberColumn("Diferencia", width="small", format="$ %d"),
            "gan%": st.column_config.NumberColumn("%", width="mediun", format='%.2f %%')
        },
        disabled=df.columns)

    # filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    if len(selected_rows) > 1:
        st.warning("Solo se puede seleccionar una fila. Seleccione solo un registro", icon="⚠️")
        return None
    if len(selected_rows) < 1:
        st.info("No se selecciono registro", icon="ℹ️")
        return None
    elif len(selected_rows) == 1:
        selected_rows = selected_rows.drop('Select', axis=1)
        return selected_rows


col1, col2 = st.columns([1, 6])
with col2:
    try:
        st.write(""" ### Detalle""")
        selection = dataframe_with_selections(df_last)
    except Exception as e:
        print(f"Error streamlit dataframe df_last: {e}")

    if selection is not None:
        id_registro_s = selection['id_registro'].iloc[0]
        fecha_compra_s = datetime.strptime(selection['fecha_compra'].iloc[0], "%Y-%m-%d").date()
        categoria_s = int(selection['categoria'].iloc[0][:1])-1
        ticker_s = selection['ticker'].iloc[0]
        cantidad_s = selection['cantidad'].iloc[0]
        monto_s = selection['monto'].iloc[0]
        st.write("Registro seleccionado:")
        st.dataframe(selection, hide_index=True)
    else:
        id_registro_s = None
        fecha_compra_s = None
        categoria_s = None
        ticker_s = None
        cantidad_s = None
        monto_s = None

with col1:
    fecha_compra = st.date_input("Fecha de compra", value=fecha_compra_s)
    categoria = st.selectbox("Categoria", ("1. FCI", "2. Cedear", "3. Accion", "4. USD"),
                             index=categoria_s,
                             placeholder="Selec instrument..."
                             )
    ticker = st.text_input("Ticker", value=ticker_s)
    cantidad = st.text_input("Cantidad", value=cantidad_s)
    monto = st.text_input("Monto", value=monto_s)

    if st.button('Cargar', type="primary", use_container_width=True):
        if fecha_compra and categoria and ticker and cantidad and monto:
            registro = Registro(
                fecha_compra,
                categoria,
                ticker.upper(),
                cantidad,
                monto
            )
            conexion = conexionDB().conexion
            guardar(registro, conexion)
            st.toast('Cargando registro... ⏳ ⌛', icon='🥳')
            time.sleep(3)
            conexion.close()
            st.rerun()
        else:
            st.warning("Registro incompleto..", icon="⚠️")

    if st.button('Editar', type="primary", use_container_width=True):
        if fecha_compra and categoria and ticker and cantidad and monto:
            registro = Registro(
                fecha_compra,
                categoria,
                ticker.upper(),
                cantidad,
                monto
            )
        if id_registro_s:
            conexion = conexionDB().conexion
            editar(registro, conexion, id_registro_s)
            st.toast('Editando registro... ⏳ ⌛', icon='😬')
            time.sleep(3)
            conexion.close()
            st.rerun()
        else:
            st.warning("No se selecciono registro! Seleccione uno..", icon="⚠️")

    if st.button('Eliminar', type="primary", use_container_width=True):
        if id_registro_s:
            conexion = conexionDB().conexion
            eliminar(id_registro_s, conexion)
            st.toast('Eliminando registro... ⏳ ⌛', icon='😤')
            time.sleep(3)
            conexion.close()
            st.rerun()
        else:
            st.warning("No se selecciono registro! Seleccione uno..", icon="⚠️")
