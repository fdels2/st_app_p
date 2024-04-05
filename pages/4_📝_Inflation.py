from utils.db_conn import conexionDB, custom_query_inf
from utils.st_def import st
from utils.functions_inf import guardar, editar, eliminar, Registro_inf
import time
from datetime import datetime


#  page config
st.set_page_config(page_title="Inflation", page_icon=":memo:", layout="wide", initial_sidebar_state="collapsed")

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

df_inf = custom_query_inf()

# page config
col1, col2 = st.columns([4, 1])
with col1:
    st.header("""Registro inflacionario""",
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
        height=(df_inf.shape[0] + 1) * 35 + 3,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=True),
            "id_registro": st.column_config.Column("Id", width="small"),
            "mes": st.column_config.Column("Mes", width="small"),
            "valor_ref": st.column_config.Column("Valor ref.", width="small")
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
        selection = dataframe_with_selections(df_inf)
    except Exception as e:
        print(f"Error streamlit dataframe df_inf: {e}")

    if selection is not None:
        id_registro_s = selection['id_registro'].iloc[0]
        mes_s = datetime.strptime(selection['mes'].iloc[0], "%Y-%m-%d").date()
        valor_ref_s = selection['valor_ref'].iloc[0]
        st.write("Registro seleccionado:")
        st.dataframe(selection, hide_index=True)
    else:
        id_registro_s = None
        mes_s = None
        valor_ref_s = None

with col1:
    mes = st.date_input("Mes", value=mes_s)
    valor_ref = st.text_input("Valor de ref", value=valor_ref_s)

    if st.button('Cargar', type="primary", use_container_width=True):
        if mes and valor_ref:
            registro = Registro_inf(
                mes,
                valor_ref
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
        if mes and valor_ref:
            registro = Registro_inf(
                mes,
                valor_ref
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
