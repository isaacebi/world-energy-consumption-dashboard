import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import plotly.express as px


def fig1(df):
    df = df.groupby('iso_code').sum().iloc[:, 1:]
    
    labels = df.columns.tolist()
    labels = ''.join(labels)
    labels = labels.split('_consumption')
    
    option = st.selectbox(
        'Select Country',
        tuple(df.index), index=6)
    
    by_country_value = df.loc[option]
    
    by_country_str = []
    for val in by_country_value:
        if val == 0:
            by_country_str.append(None)
        else:
            perc = round(val/sum(by_country_value)*100, 1)
            by_country_str.append(str(f"{perc} %"))
    
    
    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(specs=[[{'type':'domain'}]])
    
    
    fig.add_trace(go.Pie(labels=labels, values=by_country_value))
    
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+value", 
                      text=by_country_str ,textinfo='text')
    
    fig.update_layout(
        title_text=f"{option} Energy Consumption in twh 1900-2020",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=option, x=0.5, y=0.5, 
                          font_size=20, showarrow=False)])
    
    fig.update_layout(
        autosize=True,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        )
    )    
    return fig


def fig2(df):
    options = df.year.unique().tolist()
    
    start_no, end_no = st.select_slider(
        'Select range year',
        options=options,
        value=(1900, 2020))
    
    df = df.groupby('iso_code')['electricity_generation'].cumsum()[start_no:end_no]
    fig = px.bar(df)
    
    fig.update_layout(
        showlegend=False,
        autosize=True,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        )
    ) 
    return fig

def fig3(df):
    df = df.groupby('iso_code')['carbon_intensity_elec'].sum()
    
    options = st.multiselect(
        'Country',
        df.index,
        ['AFG', 'ZMB', 'ARG'])        
    
    fig = px.bar(df[options], x='carbon_intensity_elec', color=df[options].index)
    
    fig.update_layout(
        showlegend=False,
        autosize=True,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        )
    ) 
    return fig
