import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import plotly.offline as pyo
import dash_bootstrap_components as dbc

# Load the data
df = pd.read_csv('unemployment analysis.csv')

# Tidy data
c_name = []
c_code = []
year = []
unemployment_rate = []
column_names = df.columns[2:]

for index, row in df.iterrows():
    for t_year in column_names:
        c_name.append(row['Country Name'])
        c_code.append(row['Country Code'])
        year.append(t_year)
        unemployment_rate.append(row[t_year])

tidy_df = pd.DataFrame(data={'Year': year,'Country Name': c_name,'Country Code': c_code,'Unemployment Rate': unemployment_rate})
tidy_df = pd.read_csv('tidy_df.csv')

# Calculate the gap_minmax
tidy_df['gap_minmax'] = tidy_df.groupby('Country Name')['Unemployment Rate'].transform(lambda x: x.max() - x.min())
Low_gap = tidy_df.groupby('Country Name').mean('gap_minmax').sort_values('gap_minmax').index[:5]
High_gap = tidy_df.groupby('Country Name').mean('gap_minmax').sort_values('gap_minmax').index[-5:]

# Average lowest unemployment rates countries
max_value = tidy_df['Unemployment Rate'].max()

Average_L = go.Figure(go.Scatter(
    x=tidy_df.groupby('Country Name').mean('Unemployment Rate').sort_values('Unemployment Rate')['Unemployment Rate'][:10],
    y=tidy_df.groupby('Country Name').mean('Unemployment Rate').sort_values('Unemployment Rate').index[:10],
    mode='markers',
    marker=dict(color='purple')
))
Average_L.update_layout(
    title='Average Lowest Unemployment Rate',
    xaxis_title='Unemployment Rate',
    xaxis_range=[0, 1.5],
    xaxis=dict(dtick=0.5),
    height=700,
    width=600
)

# Average highest unemployment rates countries

max_value = tidy_df['Unemployment Rate'].max()

Average_H = go.Figure(go.Scatter(
    x=tidy_df.groupby('Country Name').mean('Unemployment Rate').sort_values('Unemployment Rate')['Unemployment Rate'][-10:],
    y=tidy_df.groupby('Country Name').mean('Unemployment Rate').sort_values('Unemployment Rate').index[-10:],
    mode='markers',
    marker=dict(color='blue')
))
Average_H.update_layout(
    title='Average Highest Unemployment Rate',
    xaxis_title='Unemployment Rate',
    xaxis_range=[0, 40],
    xaxis=dict(dtick=10),
    height=700,
    width=600
)



# Define the Dash app with Flask server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = html.Div([
    html.H1(children='Unemployment Rates by Country', style={'textAlign': 'center'}),
    html.Div(children='''A dashboard to explore unemployment rates by country.'''),
    dbc.Row([
    dbc.Col([
        dcc.Graph(
            id='map_graph',
            figure=px.choropleth(
                tidy_df,
                locations="Country Code",
                color="Unemployment Rate",
                hover_name="Country Name",
                animation_frame="Year",
                range_color=(0, 40),
                color_continuous_scale="Reds",
            ).update_layout(
                title=dict(
                    text="Unemployment of all countries throughout time",
                    y=0.95,
                    x=0.5,
                    xanchor='center',
                    yanchor='top'
                ),
                legend=dict(
                    x=0,
                    y=-0.2,
                    orientation='h',
                    yanchor='top',
                    font=dict(size=10),
                ),
            ),
            style={"width": "100%", "height": "600px", "overflow": "hidden"}
        ),
    ], width=12),
], style={"marginBottom": "40px"}),

        dbc.Row([
    dbc.Col([
        dcc.Graph(
            id='average_low_graph',
            figure=Average_L.update_layout(
                width=600,
                height=250,
                margin=dict(l=20, r=10, t=40, b=20),
                title=dict(
                    text="Average Low Unemployment rate",
                    x=0.55,
                    y=0.93,
                    xanchor='center',
                    yanchor='bottom',
                )
            ),
        ),
    ], width=6),
    dbc.Col([
        dcc.Graph(
            id='average_high_graph',
            figure=Average_H.update_layout(
                width=600,
                height=250,
                margin=dict(l=10, r=20, t=40, b=20),
                title=dict(
                    text="Average High Unemployment rate",
                    x=0.6,
                    y=0.93,
                    xanchor='center',
                    yanchor='bottom',
                )
            ),
        ),
    ], width=6),
]),
    html.Div([
                html.Div([
                    dcc.Graph(id='high_gap_graph',
                              figure={
                                  'data': [go.Scatter(x=tidy_df[tidy_df['Country Name'] == country]['Year'],
                                                      y=tidy_df[tidy_df['Country Name'] == country]['Unemployment Rate'],
                                                      name=country)
                                           for country in High_gap],
                                  'layout': go.Layout(xaxis=dict(rangeselector=dict(buttons=list([
                                      dict(count=1, label="1 Year", step="year", stepmode="backward"),
                                      dict(count=5, label="5 Years", step="year", stepmode="backward"),
                                      dict(count=10, label="10 Years", step="year", stepmode="backward"),
                                      dict(step="all")
                                  ])), rangeslider=dict(visible=True), type="date"),
                                                      title='Highest Volatile Countries',
                                                      xaxis_title='Year',
                                                      yaxis_title='Unemployment Rate',
                                                      width=1350,
                                                      height=400
                                                      )
                              }
                             ),
                ], className='six columns'),
                html.Div([
                    dcc.Graph(id='low_gap_graph',
                              figure={
                                  'data': [go.Scatter(x=tidy_df[tidy_df['Country Name'] == country]['Year'],
                                                      y=tidy_df[tidy_df['Country Name'] == country]['Unemployment Rate'],
                                                      name=country)
                                           for country in Low_gap],
                                  'layout': go.Layout(xaxis=dict(rangeselector=dict(buttons=list([
                                      dict(count=1, label="1 Year", step="year", stepmode="backward"),
                                      dict(count=5, label="5 Years", step="year", stepmode="backward"),
                                      dict(count=10, label="10 Years", step="year", stepmode="backward"),
                                      dict(step="all")
                                  ])), rangeslider=dict(visible=True), type="date"),
                                                      title='Lowest Volatile Countries',
                                                      xaxis_title='Year',
                                                      yaxis_title='Unemployment Rate',
                                                      width=1350,
                                                      height=400
                                                      )
                              }
                             ),
                ], className='six columns'),
            ], className='row'),
        ])


# Run the app
if __name__ == '__main__':
    port = 8891
    print(f'Starting server on port {port}...')
    app.run_server(debug=True, port=port)

