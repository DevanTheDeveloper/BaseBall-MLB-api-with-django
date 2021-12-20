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


app = DjangoDash('team_salaries')   # replaces dash.Dash
#c = open(os.path.join(workpath, 'graphs/Salaries.csv'), 'rb')
#df = pd.read_csv(c)

csv = Uploads.objects.filter(title='Salaries')
csv = csv[0].file
df = pd.read_csv(csv)
df = df[df['yearID']>=2010]
df = df[['yearID', 'teamID','playerID','salary']]
fig=px.bar(df, x='yearID', y='salary',color="teamID", title='Team Salaries Over 10years',width=800, height=400,
					labels={
						   'yearID':'Year',
						   'salary':'Salary',
						   'teamID':'Team'
										})



app.layout = html.Div(children=[
    html.Div('Team select:'),
    dcc.RadioItems(
        id='dropdown-team',
        options=[{'label': c, 'value': c} for c in df['teamID'].unique()]+
                [{'label':'Reset Chart', 'value':'reset'}],
        value='TOR'
    ),
    html.Div(id='output-team'),

    
    html.Div(id='output-result'),
    
    html.Div(id='output-mix'), 

    dcc.Graph(id='bar-plot', figure=fig)

])


@app.callback(
	dash.dependencies.Output('bar-plot', 'figure'),
	[dash.dependencies.Input('dropdown-team', 'value')])
def callback_update(dropdown_team):
	
	if dropdown_team and dropdown_team != "reset":
		mask=df[df['teamID']==dropdown_team]
		fig=px.bar(mask, x='yearID', y='salary',color='playerID', 
			title='Toronto Player Salaries Over 10years')
	else:
		mask=df
		fig=px.bar(mask, x='yearID', y='salary',color="teamID", title='Team Salaries Over 10years',
			labels={
					   'yearID':'Year',
					   'salary':'Salary',
					   'playerID':'Player'

									})
		fig.update_layout(transition_duration=200)
	return fig


@app.callback(
    dash.dependencies.Output('output-team', 'children'),
    [dash.dependencies.Input('dropdown-team', 'value')])
def callback_team(dropdown_value):
    return "The selected team is %s." % dropdown_value



