from utils.db_conn import conexionDB, custom_query_resume
from utils.st_def import mostrar_resumen_categoria, generar_espacios, categoria_label_concat_def, st
from utils.functions import actualizar, appendear_historical
from utils.df_def import last_usd_total, last_cat_ev_summ, last_cat_ev_summ_cat, hist_day_summary, agrupado_ticker_resumen, hist_day_cat_summary, last_ticker_summ
import plotly.graph_objects as go

#  page config
st.set_page_config(page_title="Resumen", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed")

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

# seteo de parametros barra lateral
st.sidebar.header('Parametros')
value = 10 if st.sidebar.toggle('//') else 1
table_suf = "_jes" if st.sidebar.toggle('Jes') else ("_mama" if st.sidebar.toggle('Mama') else "")

# DFs generation
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
df_hist, df_last = custom_query_resume(divider=value, table_suf=table_suf)
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

# DFs transformations
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
df_last_usd_total = last_usd_total(df_last=df_last)
df_last_cat_ev_summ = last_cat_ev_summ(df_last=df_last, df_hist=df_hist)
df_last_cat_ev_summ_cat = last_cat_ev_summ_cat(df_last=df_last, df_hist=df_hist)
df_hist_day_summ = hist_day_summary(df_hist=df_hist)
df_agrupado_ticker_resumen = agrupado_ticker_resumen(df_hist=df_hist)
df_hist_day_cat_summ = hist_day_cat_summary(df_hist=df_hist)
df_last_ticker_summ = last_ticker_summ(df_last=df_last)
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

# page config
espacios = generar_espacios(37)
col1, col2 = st.columns([4, 1])

with col1:
    st.header(f"""Resumen de finanzas{"*" if value>1 else ""}""",
              divider='red')
    cola, colb, colc, cold, cole = st.columns([1, 1, 1, 1, 1])
    with cola:
        try:
            st.metric(label="Portafolio", value="", delta=f"{df_last_cat_ev_summ['porcentaje_diferencia'][0]}%")
        except Exception as e:
            # print(e)
            pass
    with colb:
        try:
            st.metric(label="FCI", value="", delta=f"{df_last_cat_ev_summ_cat['porcentaje_diferencia'][0].split('%')[0]}%")
        except Exception as e:
            # print(e)
            pass
    with colc:
        try:
            st.metric(label="Cedear", value="", delta=f"{df_last_cat_ev_summ_cat['porcentaje_diferencia'][1].split('%')[0]}%")
        except Exception as e:
            # print(e)
            pass
    with cold:
        try:
            st.metric(label="Accion", value="", delta=f"{df_last_cat_ev_summ_cat['porcentaje_diferencia'][2].split('%')[0]}%")
        except Exception as e:
            # print(e)
            pass
    with cole:
        try:
            df_agrupado_ticker_resumen_categoria = df_agrupado_ticker_resumen[df_agrupado_ticker_resumen['categoria'].str.contains('USD')]
            st.metric(label="USD", value=f"${df_agrupado_ticker_resumen_categoria['valor_actual_last'].iloc[0]}", delta=f"{df_last_cat_ev_summ_cat['porcentaje_diferencia'][3].split('%')[0]}%")
        except Exception as e:
            # print(e)
            pass

with col2:
    st.header(f"""*:grey[{df_last['fecha_upd'][0]}]*""")
    if st.button('Actualizar', type="primary", use_container_width=True):
        conexion = conexionDB()
        actualizar(conexion=conexion)
        appendear_historical(conexion=conexion)
        conexion.cerrar()
        st.rerun()

#  dinamic tabs
tab_list = [tab for tab in st.tabs(['Total'] + [cat.split('. ')[1] for cat in df_last_cat_ev_summ_cat['categoria'].tolist()])]

with tab_list[0]:
    col1, col2 = st.columns([4, 1])
    with col2:
        try:
            if df_last_usd_total.shape[0]:
                st.write(""" ## Last""")
                st.dataframe(data=df_last_usd_total.drop(['categoria'], axis=1),
                             height=(df_last_usd_total.shape[0] + 1) * 35 + 3,
                             hide_index=True,
                             column_config={
                            "cantidad": st.column_config.NumberColumn("Acum", width="small", format="$ %d")
                            })
        except Exception as e:
            print(f"Error streamlit dataframe df_last_usd_total: {e}")

    with col1:
        try:
            st.write(""" ## Resumen actual""")
            st.dataframe(data=df_last_cat_ev_summ,
                         height=(df_last_cat_ev_summ.shape[0] + 1) * 35 + 3,
                         hide_index=True,
                         column_config={
                             "categoria": st.column_config.Column("", width="small"),
                             "monto": st.column_config.NumberColumn("Invertido", width="small", format="$ %d"),
                             "evolucion_invertido": st.column_config.LineChartColumn("Invertido", width="medium"),
                             "monto_actual": st.column_config.NumberColumn("Actual", width="small", format="$ %d"),
                             "evolucion_actual": st.column_config.LineChartColumn("Actual", width="medium"),
                             "porcentaje_diferencia": st.column_config.NumberColumn("%", width="small", format=f'%.2f %% {"🔴" if (df_last_cat_ev_summ["porcentaje_diferencia"] < 0).any() else "🟢"}'),
                             "diferencia_portafolio": st.column_config.NumberColumn("Dif. portafolio", width="mediun", format="$ %d"),
                             "porcentaje_dif_portafolio": st.column_config.NumberColumn("%", width="mediun", format='%.2f %%')
                            })
        except Exception as e:
            print(f"Error streamlit dataframe df_last_cat_ev_summ: {e}")

        try:
            st.write(""" ### Resumen por categoría""")
            st.dataframe(data=df_last_cat_ev_summ_cat,
                         height=(df_last_cat_ev_summ_cat.shape[0] + 1) * 35 + 3,
                         hide_index=True,
                         column_config={
                            "categoria": st.column_config.Column("Categoría", width="small"),
                            "monto_actual_sum_last": st.column_config.NumberColumn("Invertido", width="small", format="$ %d"),
                            "monto_actual_lista": st.column_config.LineChartColumn("Invertido", width="medium"),
                            "monto_sum_last": st.column_config.NumberColumn("Actual", width="small", format="$ %d"),
                            "monto_sum_lista": st.column_config.LineChartColumn("Actual", width="medium"),
                            "porcentaje_diferencia": st.column_config.TextColumn("%", width="small"),
                            "diferencia_portafolio": st.column_config.NumberColumn("Dif. portafolio", width="mediun", format="$ %d"),
                            "porcentaje_dif_portafolio": st.column_config.NumberColumn("%", width="mediun", format='%.2f %%')
                            })

            colors = ['#3E78C9', '#F1B73D', '#9959CB', '#4CBB35']
            fig = go.Figure(data=[go.Pie(labels=df_last_cat_ev_summ_cat['categoria'], values=df_last_cat_ev_summ_cat['monto_sum_last'], hole=.7, showlegend=True, textinfo='label+percent', pull=[0.2, 0.3, 0.4, 0.1], marker=dict(colors=colors))])
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig)

        except Exception as e:
            print(f"Error streamlit dataframe df_last_cat_ev_summ_cat: {e}")

    try:
        st.write("""### Evolución diaria total""")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_hist_day_summ['fecha_upd'], y=df_hist_day_summ['monto'],
                                 mode='lines',
                                 name='Total_invertido',
                                 line_shape='linear',
                                 line=dict(color="white", width=2)))
        fig.add_trace(go.Scatter(x=df_hist_day_summ['fecha_upd'], y=df_hist_day_summ['monto_actual'],
                                 mode='lines',
                                 name='Total_actual',
                                 line_shape='linear',
                                 line=dict(color='red', width=3)))
        df_hist_day_cat_summ_categoria = df_hist_day_cat_summ[df_hist_day_cat_summ['categoria'].str.contains("USD")]
        fig.add_trace(go.Scatter(x=df_hist_day_cat_summ_categoria['fecha_upd'], y=df_hist_day_cat_summ_categoria['monto'],
                                 mode='lines',
                                 name="USD_actual",
                                 line_shape='linear',
                                 line=dict(color=colors[3], width=3)))
        df_hist_day_cat_summ_categoria = df_hist_day_cat_summ[df_hist_day_cat_summ['categoria'].str.contains("Cedear")]
        fig.add_trace(go.Scatter(x=df_hist_day_cat_summ_categoria['fecha_upd'], y=df_hist_day_cat_summ_categoria['monto'],
                                 mode='lines',
                                 name="Cedear_actual",
                                 line_shape='linear',
                                 line=dict(color=colors[1], width=3)))
        df_hist_day_cat_summ_categoria = df_hist_day_cat_summ[df_hist_day_cat_summ['categoria'].str.contains("FCI")]
        fig.add_trace(go.Scatter(x=df_hist_day_cat_summ_categoria['fecha_upd'], y=df_hist_day_cat_summ_categoria['monto'],
                                 mode='lines',
                                 name="FCI_actual",
                                 line_shape='linear',
                                 line=dict(color=colors[0], width=3)))
        df_hist_day_cat_summ_categoria = df_hist_day_cat_summ[df_hist_day_cat_summ['categoria'].str.contains("Accion")]
        fig.add_trace(go.Scatter(x=df_hist_day_cat_summ_categoria['fecha_upd'], y=df_hist_day_cat_summ_categoria['monto'],
                                 mode='lines',
                                 name="Accion_actual",
                                 line_shape='linear',
                                 line=dict(color=colors[2], width=3)))

        fig.update_layout(height=500, width=1700)
        st.plotly_chart(fig)
    except Exception as e:
        print(f"Error streamlit grafico df_hist_day_summ: {e}")

    try:
        st.write(""" ### Status por compra""")
        df_last = df_last.drop(columns="fecha_upd")
        df_last['gan%'] = df_last['gan%'].apply(lambda x: f'{x:.2f}% {"🔴" if x < 0 else "🟢"}')
        st.dataframe(data=df_last,
                     height=(df_last.shape[0] + 1) * 35 + 3,
                     hide_index=True,
                     column_config={
                         "id_registro": st.column_config.Column("Id R", width="small"),
                         "fecha_compra": st.column_config.Column("Fecha Compra", width="mediun"),
                         "categoria": st.column_config.Column("Categoría", width="small"),
                         "ticker": st.column_config.Column("Ticker", width="small"),
                         "cantidad": st.column_config.NumberColumn("Cant", width="small", format="%.2f"),
                         "monto": st.column_config.NumberColumn("Monto", width="mediun", format="$ %.2f"),
                         "valor_actual": st.column_config.NumberColumn("V. actual", width="small", format="$ %.2f"),
                         "monto_actual": st.column_config.NumberColumn("Monto act", width="mediun", format="$ %.2f"),
                         "diferencia": st.column_config.NumberColumn("Diferencia", width="mediun", format="$ %.2f"),
                         "gan%": st.column_config.TextColumn("%", width="mediun")
                     })

    except Exception as e:
        print(f"Error streamlit dataframe df_last: {e}")

try:
    with tab_list[1]:
        color = categoria_label_concat_def.get("FCI").split("/")
        mostrar_resumen_categoria("FCI", df_last, df_last_cat_ev_summ_cat, df_agrupado_ticker_resumen, df_hist_day_cat_summ, df_last_ticker_summ, color)
except Exception as e:
    # print(e)
    pass

try:
    with tab_list[2]:
        color = categoria_label_concat_def.get("Cedear").split("/")
        mostrar_resumen_categoria("Cedear", df_last, df_last_cat_ev_summ_cat, df_agrupado_ticker_resumen, df_hist_day_cat_summ, df_last_ticker_summ, color)
except Exception as e:
    # print(e)
    pass

try:
    with tab_list[3]:
        color = categoria_label_concat_def.get("Accion").split("/")
        mostrar_resumen_categoria("Accion", df_last, df_last_cat_ev_summ_cat, df_agrupado_ticker_resumen, df_hist_day_cat_summ, df_last_ticker_summ, color)
except Exception as e:
    # print(e)
    pass

try:
    with tab_list[4]:
        color = categoria_label_concat_def.get("USD").split("/")
        mostrar_resumen_categoria("USD", df_last, df_last_cat_ev_summ_cat, df_agrupado_ticker_resumen, df_hist_day_cat_summ, df_last_ticker_summ, color)
except Exception as e:
    # print(e)
    pass
