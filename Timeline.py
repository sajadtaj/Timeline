# Add  
#--------------------------------------------------------------------+
#                               Import library                       |
#--------------------------------------------------------------------+
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st


#--------------------------------------------------------------------+
#                         Set Root Direction                         |
#--------------------------------------------------------------------+
import os 
# os.chdir(rf'E:\Prefessional  Python\Clone From Git\Timeline')   # Work
os.chdir(rf'D:\My Code\Github\Timeline')   # Home
#-------------------------------------+
#            Page configs             |
#-------------------------------------+
st.set_page_config(
    page_title="Timeline",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 0rem;
                    padding-left: 3rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)
#--------------------------------------------------------------------+
#                               Read Files                           |
#--------------------------------------------------------------------+
gold = pd.read_pickle(rf'Data\CleanData.csv') 

#--------------------------------------------------------------------+
#                           Preperation Data                         |
#--------------------------------------------------------------------+

start_date = st.sidebar.date_input(
    label="Start Date",
    value=datetime.date(2019, 1, 2),
    min_value = datetime.date(2019, 1, 2),
    max_value = datetime.date(2021, 4, 22),
    )
end_date = st.sidebar.date_input(
    label="End Date",
    value=datetime.date(2021, 4, 22),
    min_value = datetime.date(2019, 1, 2) ,
    max_value = datetime.date(2021, 4, 22),
    )

start = gold[gold['Date'].values  > start_date.strftime("%Y-%m-%d") ]
end   = start[start['Date'].values < end_date.strftime("%Y-%m-%d")    ]
price = end.copy()

# line price in price DataFrame
price.reset_index(inplace=True)

# Event point in justnews DataFrame
justnews=end.dropna()
All_Events = justnews['Description'].unique()
Select_event = st.sidebar.selectbox("Select Event", All_Events)
justnews = justnews[justnews['Description']== Select_event]
#--------------------------------------------------------------------+
#                            Fiugure page 1                          |
#--------------------------------------------------------------------+
fig = go.Figure()
annotations=[]
fig.add_trace(go.Scatter(x=end['Date'], y=end['Close'],
                    mode='lines',
                    name='Price'))
fig.add_trace(go.Scatter(x=justnews['Date'], y=justnews['Close'],
                    mode='markers',
                    name='Event',
                    line=dict(color='firebrick', width=4,
                              dash='dash'),                    
                    )
 )
for index, row in justnews.iterrows():
        annotations.append( dict(
                            # title = 'Gold Price Time',
                            text=row['Description'],
                            x=row['Date'],
                            y=row['Close'],
                            xref="x", 
                            yref="y",
                            showarrow=True,
                            ax=0,
                            ay=-(row['Close'] / 70),
                            arrowcolor ='#999999',
                            arrowsize=0.3,
                            arrowwidth=1.4,
                            bordercolor='#A0C49D',
                            captureevents =True,
                            opacity = 0.7,
                            hovertext=f" Actual:{row['Actual event']} \t  Evaluation:{row['Evaluation data']} ",
                            clicktoshow="onoff",
                            
                            xanchor= 'auto',
                            yanchor = 'bottom',
                            arrowhead= 1,
                            arrowside ='start' ,
                            borderpad=5,
                            borderwidth=0,  
                            
                            hoverlabel= dict(
                                bgcolor='#DDE6ED',
                                bordercolor='#19376D',
                            ),
                            font=dict(
                                color='#19376D',
                                family="Balto",
                                size=11
                            )
                            
                            
                            )
        )

fig.update_layout(annotations=annotations)
fig.update_layout(
    autosize=True,
    width=1300,
    # height=750,
    margin=dict(l=0, r=0, t=30, b=0)
    )



#--------------------------------------------------------------------+
#                            Streamlit config                        |
#--------------------------------------------------------------------+


#-------------------------------------+
#              Set Tabs               |
#-------------------------------------+

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

# st.plotly_chart(fig)

tab1.subheader("Gold Price + Event")
tab1.plotly_chart(fig)

tab2.subheader("DataFrame")
tab2.write(justnews)