#importing libraries
import plotly.express as px
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import json
import calendar


#Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, 'assets/style.css'])
app.title = 'Minority Report'
server = app.server


#reading dataset
ds = pd.read_csv('datasets/sanFran_clean.csv')


dsmap = ds.district.value_counts()
ds_viz = pd.DataFrame(data=dsmap.values, index=dsmap.index, columns=['Count'])
ds_viz = ds_viz.reindex(["CENTRAL", "NORTHERN", "PARK", "SOUTHERN", "MISSION", "TENDERLOIN", "RICHMOND", "TARAVAL", "INGLESIDE", "BAYVIEW"])
ds_viz = ds_viz.reset_index()
ds_viz.rename({'index': 'Neighborhood', 'Count': 'Arrests'}, axis='columns', inplace=True)
df = ds_viz


ds_unique = ds[['day', 'district']]
ds_unique = ds_unique.groupby(["day", "district"]).size().reset_index(name="Crime Frequency")

district_options = []
for district in ds_unique['district'].unique():
    district_options.append({'label':str(district),'value':district})


#figure 1
with open('datasets/san-francisco.geojson') as f:
    gjson = json.load(f)

fig_map = px.choropleth(df, geojson = gjson, color="Arrests", locations="Neighborhood", 

                    featureidkey="properties.DISTRICT")
fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(
    margin={"r":10, "t":10, "l":10, "b":10}, 
    height=600, 
    template="plotly_dark", 
    title={
        'text': "Number of Arrests in San Francisco Neighborhoods",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)


# table 3
ds3 = ds[['month', 'district']]
ds3 = ds3.groupby(["month", "district"]).size().reset_index(name="Crime Frequency")
ds3['month'] = ds3['month'].apply(lambda x: calendar.month_abbr[x])


# table 4
ds4 = ds[['year', 'district']]
ds4 = ds4.groupby(["year", "district"]).size().reset_index(name="Crime Frequency")

# figure 4
fig_4 = px.line(ds4, x='year', y='Crime Frequency', color='district')
fig_4.update_layout(
    margin={"r":20, "t":20, "l":20, "b":20}, 
    template="plotly_dark", 
    title={
        'text': "Crime Frequency from 2003 to 2018",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)


# table 5
ds5 = ds[ds.result != "NONE"]
ds5 = pd.DataFrame(ds5.result.value_counts()).reset_index()

# figure 5
fig_ind = go.Figure()

fig_ind.add_trace(
    go.Indicator(
        mode = "number",
        value = ds5['result'][0].round(1),
        number={"font":{"size":60}},
        title = {"text": ds5['index'][0]},
        domain = {'row': 0, 'column': 0},
    ),
)

fig_ind.add_trace(
    go.Indicator(
        mode = "number",
        value = ds5['result'][1].round(1),
        number={"font":{"size":60}},
        title = {"text": ds5['index'][1]},
        domain = {'row': 0, 'column': 1},
    ),
)

fig_ind.add_trace(
    go.Indicator(
        mode = "number",
        value = ds5['result'][2].round(1),
        number={"font":{"size":60}},
        title = {"text": ds5['index'][2]},
        domain = {'row': 0, 'column': 2},
    ),
)

fig_ind.update_layout(
    grid = {'rows': 1, 'columns': 3}, 
    template="plotly_dark", 
    margin={"r":20, "t":30, "l":0, "b":0}
)


##Layout of the application
app.layout = html.Div([

    dbc.Row([
        dbc.Col(
            [
                html.Div(
                    [
                        html.H3("Minority Report"),
                        html.H6("San Francisco Police Department's Guide for Smart Police Patrolling"),
                    ],
                ),
            ],
            className="h-50", 
            style = {
                'text-align':'center',
                'color':'white', 
                'width':'38%',
                'display': 'inline-block',
                'padding-right':'5px',
                }, 
        ),

        dbc.Col([
            
            html.Div(
                [
                    dcc.Graph(
                        id='indicator1', 
                        figure=fig_ind, 
                        style = {
                            'height':'130px',
                            },
                        ),
                    ],
                ),
        ],
            style = {
                'width':'58%', 
                'text-align':'center', 
                'padding-left':'5px',
                'display': 'inline-block',
                },
            ),
        ],
        justify="center", 
        align="center", 
        style = {
            'margin-bottom':'10px',
            'padding-top':'15px',
            },
    ),

    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div([
                        dcc.Graph(
                            id='graph1',
                            figure=fig_map
                        ),
                ],),
            ],
                style = {
                    'width': '38%', 
                    'display': 'inline-block', 
                    'margin-bottom':'10px', 
                    'padding-right':'5px',
                    },
            ),

            dbc.Col(
                [
                    dcc.Dropdown(
                        id='district-picker', 
                        options=district_options, 
                        value=ds_unique['district'][0], 
                        style = {
                            'color':'black', 
                            'margin-bottom':'10px',
                            },
                        ),
                    
                    dcc.Graph(
                        id='graph2', 
                        style = {
                            'height':'44.5%', 
                            'margin-bottom':'10px',
                            },
                        ),
                    
                    dcc.Graph(
                        id='graph3',
                        style = {
                            'height':'44.5%',
                            },
                        ),
                    ], 
                
                style = {
                    'width': '58%', 
                    'padding-left':'5px',
                    },
                ),
    ],),

    dbc.Row(
        dcc.Graph(
            id='graph4', 
            figure=fig_4,
            ),
        
        style = {
            'padding-right':'15px', 
            'padding-left':'15px',
            'padding-bottom':'15px', 
            'width':'100%', 
            'display': 'inline-block',
            },
    ),
    
], style = {
    "background-color":"#383636",
    'color':'white',
    },
)


@app.callback(Output('graph2','figure'),
            [Input('district-picker','value')])
def update_figure(selected_district):
    mask = ds_unique["district"] == selected_district
    fig = px.bar(
        ds_unique[mask], 
        x = 'day', 
        y = 'Crime Frequency', 
        category_orders={
            "day": [
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
                ],
            },
        )
    fig.update_layout(
        margin={
            "r":20, 
            "t":20, 
            "l":20, 
            "b":20
            }, 
        template="plotly_dark",
        title={
            'text': "Crime Frequency per Day",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    return fig


@app.callback(Output('graph3','figure'),
            [Input('district-picker','value')])
def update_figure(selected_district):
    mask = ds3["district"] == selected_district
    fig = px.bar(
        ds3[mask], 
        x = 'month', 
        y = 'Crime Frequency',
        color_discrete_sequence = ['#7b2cbf']
        )
    fig.update_layout(
        margin={
            "r":20, 
            "t":20, 
            "l":20, 
            "b":20
            }, 
        template="plotly_dark",
        title={
            'text': "Crime Frequency per Month",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    return fig


if __name__ == '__main__':
    app.run_server()

