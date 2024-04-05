import streamlit as st
import plotly.graph_objects as go


categoria_label_concat_def = {
    "Accion":   ":violet/#9959CB",
    "Cedear":   ":orange/#F1B73D",
    "USD":      ":green/#4CBB35",
    "FCI":      ":blue/#3E78C9"
    }


def generar_espacios(n):
    """Generate a string containing n non-breaking spaces.

    Args:
        n (int): The number of non-breaking spaces to generate.

    Returns:
        str: A string containing n non-breaking spaces.
    """
    return "&nbsp;" * n


def mostrar_resumen_categoria(categoria, df_last, df_agrupado_bis, df_agrupado_ticker_resumen, df_hist_day_cat_summ, df_last_ticker_summ, color):
    """Display a summary of financial data for a specific category.

    Args:
        categoria (str): The category to display the summary for.
        df_last (DataFrame): DataFrame containing the last financial data.
        df_agrupado_bis (DataFrame): DataFrame containing aggregated data.
        df_agrupado_ticker_resumen (DataFrame): DataFrame containing summarized data for tickers.
        df_hist_day_cat_summ (DataFrame): DataFrame containing historical daily summary data.
        df_last_ticker_summ (DataFrame): DataFrame containing the last summarized data for tickers.
        color (tuple): A tuple containing color information for visualization.

    Returns:
        None
    """
    try:
        st.write(f"""## Resumen actual de {color[0]}[*{categoria}*]""")

        df_agrupado_bis_categoria = df_agrupado_bis[df_agrupado_bis['categoria'].str.contains(categoria)]

        st.dataframe(data=df_agrupado_bis_categoria,
                     hide_index=True,
                     height=(df_agrupado_bis_categoria.shape[0] + 1) * 35 + 3,
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
    except Exception as e:
        print(f"Error streamlit dataframe df_agrupado_bis_{categoria}: {e}")

    try:
        st.write("""### Resumen por ticker""")

        df_agrupado_ticker_resumen_categoria = df_agrupado_ticker_resumen[df_agrupado_ticker_resumen['categoria'].str.contains(categoria)]
        df_agrupado_ticker_resumen_categoria = df_agrupado_ticker_resumen_categoria.drop(['categoria'], axis=1)

        df_agrupado_ticker_resumen_categoria['porcentaje_diferencia'] = df_agrupado_ticker_resumen_categoria['porcentaje_diferencia'].apply(
            lambda x: f'{x:.2f}% {"🔴" if x < 0 else "🟢"}')

        st.dataframe(data=df_agrupado_ticker_resumen_categoria,
                     hide_index=True,
                     height=(df_agrupado_ticker_resumen_categoria.shape[0] + 1) * 35 + 3,
                     column_config={
                         "ticker": st.column_config.Column("Tiecker", width="small"),
                         "valor_actual_last": st.column_config.NumberColumn("Last", width="small", format="$ %.2f"),
                         "valor_actual_last_lista": st.column_config.LineChartColumn("Variación precio", width="medium"),
                         "porcentaje_diferencia": st.column_config.TextColumn("%", width="small")
                     })
    except Exception as e:
        print(f"Error streamlit dataframe df_agrupado_ticker_resumen_{categoria}: {e}")

    try:
        st.write(f"""### Evolución diaria total de {color[0]}[*{categoria}*]""")

        df_hist_day_cat_summ_categoria = df_hist_day_cat_summ[df_hist_day_cat_summ['categoria'].str.contains(categoria)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_hist_day_cat_summ_categoria['fecha_upd'], y=df_hist_day_cat_summ_categoria['monto'],
                                 mode='lines',
                                 name=categoria+"_actual",
                                 line_shape='linear',
                                 line=dict(color=color[1], width=3)))
        fig.add_trace(go.Scatter(x=df_hist_day_cat_summ_categoria['fecha_upd'], y=df_hist_day_cat_summ_categoria['monto_actual'],
                                 mode='lines',
                                 name=categoria+"_invertido",
                                 line_shape='linear',
                                 line=dict(color='white', width=2)))

        fig.update_layout(height=500, width=1700)
        st.plotly_chart(fig)
    except Exception as e:
        print(f"Error streamlit grafico df_hist_day_cat_summ_{categoria}: {e}")

    try:
        df_last_ticker_summ = df_last_ticker_summ[df_last_ticker_summ['categoria'].str.contains(categoria)]
        fig = go.Figure(data=[go.Pie(labels=df_last_ticker_summ['ticker'], values=df_last_ticker_summ['monto'], hole=.7, showlegend=True, textinfo='label+percent')])
        fig.update_layout(height=400, width=600)
        st.plotly_chart(fig)
    except Exception as e:
        print(f"Error streamlit grafico df_last_ticker_summ_{categoria}: {e}")

    try:
        st.write(f"""### Resumen de ganacia por compra de {color[0]}[*{categoria}*]""")

        df_last = df_last[df_last['categoria'].str.contains(categoria)]

        st.dataframe(data=df_last[['id_registro', 'fecha_compra', 'ticker', 'monto', 'monto_actual', 'diferencia', 'gan%']],
                     hide_index=True,
                     height=(df_last.shape[0] + 1) * 35 + 3,
                     column_config={
                         "id_registro": st.column_config.Column("Id", width="small"),
                         "fecha_compra": st.column_config.Column("F. compra", width="small"),
                         "ticker": st.column_config.Column("Ticker", width="small"),
                         "monto": st.column_config.NumberColumn("Invertido", width="mediun", format="$ %.2f"),
                         "monto_actual": st.column_config.NumberColumn("M. actual", width="mediun", format="$ %.2f"),
                         "diferencia": st.column_config.NumberColumn("Diferencia", width="mediun", format="$ %.2f"),
                         "gan%": st.column_config.TextColumn("%", width="mediun")
                     }
                     )
    except Exception as e:
        print(f"Error streamlit grafico df_last_{categoria}: {e}")
