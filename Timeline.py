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
os.chdir(rf'E:\Prefessional  Python\Clone From Git\Timeline')
#-------------------------------------+
#            Page configs             |
#-------------------------------------+
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

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

st.title(start_date.strftime("%Y-%m-%d"))
st.title(end_date.strftime("%Y-%m-%d"))
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
                            hovertext=f"{row['Description']} \n {row['Close']}",
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
                                size=8
                            )
                            
                            
                            )
        )

fig.update_layout(annotations=annotations)



#--------------------------------------------------------------------+
#                            Streamlit config                        |
#--------------------------------------------------------------------+


#-------------------------------------+
#              Set Tabs               |
#-------------------------------------+

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

# st.plotly_chart(fig)

tab1.subheader("A tab with a chart")
tab1.plotly_chart(fig)

tab2.subheader("A tab with the data")
tab2.write(justnews)