import numpy as np
import plotly.graph_objs as go
import plotly.offline as ply
import pandas as pd
import os

###############################
# Sets directory to the directory where this file is found.
os.chdir(os.path.dirname(os.path.realpath(__file__)))

df = pd.read_csv('csv/hbcy-ev-100-1/minute.csv')

df.head()
trace = go.Scatter(
                  x = df['timestamp'], y = df['temp_internal_number'],
                  name='Minute values',
                  fill= None,
                  mode='lines',
                  line=dict(
                    color='#30aa55',
                    shape="spline",
                    width=3,
                     )
                  )
 
'''
trace_low = go.Scatter(
                x = df['time'], y = df['low'],
                name='Hourly Low',
                fill='tonexty',
                fillcolor = '#212e4f',
                mode='lines',
                line=dict(
                color='rgb(45, 118, 175)',
                     )
                )
'''

layout = go.Layout(
                title='Internal Temperature',
                plot_bgcolor='#1b2023', 
                showlegend=False,
                margin=go.Margin(
                    l=40,
                    r=00,
                    b=50,
                    t=50,
                    pad=4
                    ),
                paper_bgcolor='#1b2023',
                font=dict(size=12, color='#a1b4b4'),
                )

fig = go.Figure(data=[trace], layout=layout, )
config={'showLink': False, 
        'displayModeBar': False}

div = ply.plot(fig, config=config, filename='hbcy-temp.html')

'''
print(div)


, include_plotlyjs=False, output_type='div'
'''