from utils.db_conn import custom_query_inf
from utils.st_def import generar_espacios, st
from utils.df_def import inf_mensual, inf_interanual, inf_acumulado
import plotly.graph_objects as go
import plotly.express as px


#  configuracion de pagina
st.set_page_config(page_title="Resumen inflacion", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed")

#  configuracion barra lateral
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

# DFs generation
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
df_inf = custom_query_inf()
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

# DFs transformations
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
df_inf_men = inf_mensual(df=df_inf)
df_inf_men_iter = inf_interanual(df=df_inf_men)
df_inf_men_iter_acum = inf_acumulado(df=df_inf_men_iter)
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

# page config
espacios = generar_espacios(37)
col1, col2, col3, col4 = st.columns([12, 1, 1, 1])

with col1:
    st.header("""Resumen de inflación""",
              divider='red')
st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
with col2:
    try:
        st.metric(label="Last mensual", value="", delta_color="off", delta=f"{df_inf_men_iter_acum['ipc_mensual'].iloc[-1]}%")
    except Exception as e:
        # print(e)
        pass
with col3:
    try:
        st.metric(label="Last acumulado", value="", delta_color="off", delta=f"{df_inf_men_iter_acum['ipc_acum'].iloc[-1]}%")
    except Exception as e:
        # print(e)
        pass
with col4:
    try:
        st.metric(label="Last interanual", value="", delta_color="off", delta=f"{df_inf_men_iter_acum['ipc_interanual'].iloc[-1]}%")
    except Exception as e:
        # print(e)
        pass

colors = px.colors.sequential.YlOrRd

fig = go.Figure(data=[go.Bar(x=df_inf_men_iter_acum['mes'], y=df_inf_men_iter_acum['ipc_mensual'], text=df_inf_men_iter_acum['ipc_mensual'], textfont=dict(size=18, color='black'), marker=dict(color=df_inf_men_iter_acum['ipc_mensual'], colorscale=colors))])
fig.update_layout(height=500, width=1600)
st.plotly_chart(fig)

fig = go.Figure(data=[go.Bar(x=df_inf_men_iter_acum['mes'], y=df_inf_men_iter_acum['ipc_acum'], text=df_inf_men_iter_acum['ipc_acum'], textfont=dict(size=18, color='black'), marker=dict(color=df_inf_men_iter_acum['ipc_acum'], colorscale=colors))])
fig.update_layout(height=500, width=1600)
st.plotly_chart(fig)

fig = go.Figure(data=[go.Bar(x=df_inf_men_iter_acum['mes'], y=df_inf_men_iter_acum['ipc_interanual'], text=df_inf_men_iter_acum['ipc_interanual'], textfont=dict(size=18, color='black'), marker=dict(color=df_inf_men_iter_acum['ipc_interanual'], colorscale=colors))])
fig.update_layout(height=500, width=1600)

st.plotly_chart(fig)
