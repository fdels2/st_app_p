from functions import actualizar, appendear_historical
from db_conn import conexionDB
from telegram_post import telegram_bot_sendtext
from db_conn import custom_query_resume
from df_def import last_usd_total, last_cat_ev_summ, last_cat_ev_summ_cat, hist_day_summary, agrupado_ticker_resumen, hist_day_cat_summary, last_ticker_summ

conexion = conexionDB()
actualizar(conexion)
appendear_historical(conexion)
conexion.cerrar()


# DFs generation
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
df_hist, df_last = custom_query_resume(divider=1, table_suf="")
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

df_agrupado_ticker_resumen_categoria = df_agrupado_ticker_resumen[df_agrupado_ticker_resumen['categoria'].str.contains('USD')]

# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

telegram_msj = f"""Fecha de actualizacion: _{df_last['fecha_upd'][0]}_\n
*Portafolio: {df_last_cat_ev_summ['porcentaje_diferencia'][0]}%  {"🟢" if df_last_cat_ev_summ['porcentaje_diferencia'][0]>0 else "🔴"}*\n
-------- Resumen por instrumento --------
FCI: {df_last_cat_ev_summ_cat['porcentaje_diferencia'][0].split('%')[0]}% {"🟢" if float(df_last_cat_ev_summ_cat['porcentaje_diferencia'][0].split('%')[0])>0 else "🔴"}
Cedear: {df_last_cat_ev_summ_cat['porcentaje_diferencia'][1].split('%')[0]}% {"🟢" if float(df_last_cat_ev_summ_cat['porcentaje_diferencia'][1].split('%')[0])>0 else "🔴"}
Accion: {df_last_cat_ev_summ_cat['porcentaje_diferencia'][2].split('%')[0]}% {"🟢" if float(df_last_cat_ev_summ_cat['porcentaje_diferencia'][2].split('%')[0])>0 else "🔴"}
USD (${df_agrupado_ticker_resumen_categoria['valor_actual_last'].iloc[0]}): {df_last_cat_ev_summ_cat['porcentaje_diferencia'][3].split('%')[0]}% {"🟢" if float(df_last_cat_ev_summ_cat['porcentaje_diferencia'][3].split('%')[0])>0 else "🔴"}
-------------------------------------------------------------"""

telegram_bot_sendtext(telegram_msj)
