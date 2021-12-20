import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import plotly.express as px

from .models import Uploads

#workpath = os.path.dirname(os.path.abspath(__file__))


app = DjangoDash('team_stats')   # replaces dash.Dash
#c = open(os.path.join(workpath, 'graphs/Teams.csv'), 'rb')
#df = pd.read_csv(c)
csv = Uploads.objects.filter(title='team stats')
csv = csv[0].file
df = pd.read_csv(csv)


df = df[df['yearID']>=2010]
df = df[['yearID', 'teamID','W','L']]
fig = px.line(df, x="yearID", y="W", color='teamID', title='All Team Wins 2010-2020',
              labels={
                        'yearID':'Year',
                        'W':'Wins',
                        'teamID':'Team'
              }  )



app.layout = html.Div([
    html.Div('Team select:'),
    dcc.RadioItems(
        id='dropdown-team',
        options=[{'label': c, 'value': c} for c in df['teamID'].unique()]+
                [{'label':'Reset Chart', 'value':'reset'}],
        value=None
    ),
    html.Div(id='output-team'),

    dcc.RadioItems(
        id='dropdown-result',
        options=[{'label': 'Win','value': 'W'},
                  {'label': 'Loss','value': 'L'}],
        value='W'
    ),
    html.Div(id='output-result', style={'font-weight':'bold'}),
    
    html.Div(id='output-mix', style={'font-weight':'bold'}), 

    dcc.Graph(id='line_plot', figure=fig)

])


@app.callback(
    dash.dependencies.Output('line_plot', 'figure'),
    [dash.dependencies.Input('dropdown-result', 'value'),
     dash.dependencies.Input('dropdown-team', 'value')])
def callback_result(dropdown_result,dropdown_team):
    if dropdown_team and dropdown_team != 'reset':
        mask=df[df['teamID']==dropdown_team]
    else:
        mask=df
    fig = px.line(mask, x="yearID", y=dropdown_result, color='teamID', title="All Team %s's 2010-2020" % dropdown_result,
              labels={
                        'yearID':'Year',
                        'W':'Wins',
                        'teamID':'Team',
                        'L':'Losses'
                })
    fig.update_layout(transition_duration=200)
    return fig


@app.callback(
    dash.dependencies.Output('output-team', 'children'),
    [dash.dependencies.Input('dropdown-team', 'value')])
def callback_team(dropdown_value):
    return "The selected team is %s." % dropdown_value



@app.callback(
    dash.dependencies.Output('output-mix', 'children'),
    [dash.dependencies.Input('dropdown-team', 'value'),
     dash.dependencies.Input('dropdown-result', 'value')])
def callback_mix(dropdown_team, dropdown_result):
    return "Currently displaying: Team %s and %s results." %(dropdown_team,
                                                  dropdown_result)








'''
class practice():
    app = DjangoDash('SimpleExample')   # replaces dash.Dash

    app.layout = html.Div([
        dcc.RadioItems(
            id='dropdown-color',
            options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
            value='red'
        ),
        html.Div(id='output-color'),
        dcc.RadioItems(
            id='dropdown-size',
            options=[{'label': i,
                      'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
            value='medium'
        ),
        html.Div(id='output-size')

    ])

    @app.callback(
        dash.dependencies.Output('output-color', 'children'),
        [dash.dependencies.Input('dropdown-color', 'value')])
    def callback_color(dropdown_value):
        return "The selected color is %s." % dropdown_value

    @app.callback(
        dash.dependencies.Output('output-size', 'children'),
        [dash.dependencies.Input('dropdown-color', 'value'),
         dash.dependencies.Input('dropdown-size', 'value')])
    def callback_size(dropdown_color, dropdown_size):
        return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                      dropdown_color)'''



