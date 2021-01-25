import sqlite3

import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------------------------

@st.cache
def read_data():
    ##CHANGE##
    conn = sqlite3.connect('/database/cricinfo_raw.db')
    data = pd.read_sql("SELECT * FROM raw",conn)

    return data


d = read_data()

st.header('''Cric Analysis''')

select_type = st.selectbox('Bowling or Batting stat?', ['Batting','Bowling'])

if select_type == 'Batting':
    st.subheader('Select player')
    select_player = st.selectbox('Player', d['batsman'].unique().tolist())
    
    bat = d[d['batsman']==select_player].copy()

    st.write("Overall Performance")
    bat = bat[bat['runScored'] != ' OUT']
    bat['runScored']  = bat['runScored'].astype('int')
    out = bat.groupby(['bowler']).agg({'runScored':'sum','ball':'count'})
    st.write(out)
