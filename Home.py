import streamlit as st
import datetime


st.set_page_config(page_title="Home", page_icon=":money_with_wings:", layout="wide", initial_sidebar_state="collapsed")
#  Barra lateral
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

col1, col2 = st.columns([4, 1])

with col1:
    st.header("""Home 💸""",
              divider='red')
    st.page_link("pages/1_📊_Resumen.py", label="1 - Resumen", icon="📊")
    st.page_link("pages/2_📝_Finance_inv.py", label="2 - Finance inv", icon="📝")
    st.page_link("pages/3_📊_Resumen_inf.py", label="3 - Resumen inflación", icon="📊")
    st.page_link("pages/4_📝_Inflation.py", label="4 - Inflation", icon="📝")

with col2:
    st.header(f"""*:grey[{datetime.date.today()}]*""")
