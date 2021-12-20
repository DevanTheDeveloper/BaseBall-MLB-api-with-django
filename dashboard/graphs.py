from plotly.offline import plot
from plotly import graph_objects as go
import os
import pandas as pd
import plotly.express as px

workpath = os.path.dirname(os.path.abspath(__file__))

def player_salaries():
	c = open(os.path.join(workpath, 'graphs/Salaries.csv'), 'rb')
	df = pd.read_csv(c)
	df=df [(df['teamID'] == 'TOR') & (df['yearID']>=2010)]
	figure=px.bar(df, x='yearID', y='salary',color="playerID", title='Toronto Player Salaries Last 6 Yrs')
	
	return figure.to_html()


def team_wins():
	c = open(os.path.join(workpath, 'graphs/Teams.csv'), 'rb')
	df = pd.read_csv(c)
	df = df.head(100)
	figure = px.bar(df, x='teamID', y='W', color='teamID', title=' All Team Wins - 2020'  )
	
	return figure.to_html()


def team_wins_over():
	c = open(os.path.join(workpath, 'graphs/Teams.csv'), 'rb')
	df = pd.read_csv(c)
	df=df[df['yearID']>=2010]
	figure = px.line(df, x='yearID', y='W', color='teamID', title='All Team Wins 2010-2020'  )
	return figure.to_html()







def long_version():
	x1 = [1,2,3,4,5]
	y1 = [10,20,30,40,50]

	trace = go.Scatter(
					x = x1,
					y = y1
				)



	layout = dict(
			title='Example',
			xaxis= dict(range=[min(x1),max(x1)]),
			yaxis= dict(range=[min(y1),max(y1)])

		)


	fig = go.Figure(data=[trace], layout=layout)

	plot_div = plot(fig, output_type='div')

	return plot_div