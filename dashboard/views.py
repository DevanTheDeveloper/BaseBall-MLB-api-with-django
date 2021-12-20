
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import graphs as graphs
from . import team_stats
from . import player_salaries

from .models import Uploads

from .forms import FileForm

import requests
import pandas as pd

# Create your views here.




# Create your views here.

BASE = "https://statsapi.mlb.com/"
BALL_PARK = "https://prod-gameday.mlbstatic.com/responsive-gameday-assets/1.2.0/images/fields/"#id.svg




def playerView(request,teamID, playerID):
	if request.method == "GET" and playerID:
		context = {
					'playerData':{'profile':{},
								  'stats':{}},
					'teamData':{}
		}
		playerProfile = requests.get(BASE+'/api/v1/people/{}?hydrate=stats(group=[hitting,pitching,fielding],type=[yearByYear])'.format(playerID)).json()['people'][0]
		
		teamData = requests.get(BASE + '/api/v1/teams/{}'.format(teamID)).json()['teams'][0]

		for key, value in teamData.items():
			context['teamData'][key] = value


		for key,value in playerProfile.items():
			context['playerData']['profile'][key] = value

		if 'stats' in list(playerProfile.keys()):
			playerStats = playerProfile['stats']
			for statGroup in playerStats:
				context['playerData']['stats'][statGroup['group']['displayName']] = statGroup['splits']

		return render(request, 'website/player_profile.html', context)



def rosterView(request,teamID):
	if request.method == "GET":
		if teamID:

			context = {'rosterData':{},
						'teamData':{},
						'springVenue':{},

							}

			teamData = requests.get(BASE + '/api/v1/teams/{}'.format(teamID)).json()['teams'][0]

			for key, value in teamData.items():
				context['teamData'][key] = value

			rosterData=requests.get(BASE + '/api/v1/teams/{}/roster'.format(teamID)).json()['roster']

			for player in rosterData:
				context['rosterData'][player['person']['fullName']]={}
				for key, value in player.items():
					context['rosterData'][player['person']['fullName']][key] = value
			
			springVenueID = teamData['springVenue']['id']
		
			springData=requests.get("https://statsapi.mlb.com/api/v1/venues/{}".format(springVenueID)).json()['venues'][0]
			
			for key,value in springData.items():
				context['springVenue'][key]=value

			return render(request, 'website/roster.html', context)



def index(request):
	context = {'teams':{}}
	
	res = requests.get(BASE+'/api/v1/teams?sportId=1').json()['teams']
	df = pd.DataFrame(res)


	for index,row in df.iterrows():
		context['teams'][index] = {
				'id':row['id'],
				'name': row['name'],
				'location':row['locationName'],
				'link':row['link'],
				'season':row['season'],
				'venue':row['venue'],
				'springVenue':row['springVenue'],
	            'allStarStatus':row['allStarStatus'],
				'active':row['active'],
				'abbreviation':row['abbreviation'],

				}

	if request.method == "GET":

		
		
		return render(request, 'website/index.html', context)

	else:

		context={}
		return render(request, 'website/index.html', context)




def homepage(request):
	if request.method == "GET":

		
		context={'plot1':graphs.player_salaries(),
				 #'plot2':team_wins(),	
				# 'plot3':team_wins_over()

				 					}
		return render(request, 'website/homepage.html', context)

	else:

		context={}
		return render(request, 'website/homepage.html', context)


def dashboard(request):
	if request.method == "GET":

		
		context={}
		return render(request, 'website/index.html', context)

	else:

		context={}
		return render(request, 'website/index.html', context)



def team_stats(request):
	if request.method == "GET":
		context={}

	return render(request, 'website/team_stats.html',context)

def team_salaries(request):
	if request.method == "GET":
		context={}

	return render(request, 'website/team_salaries.html',context)



def upload_file(request):

	context={'form':FileForm(),
		 'uploads':Uploads.objects.all().order_by('-date')}
	if request.method == 'POST':
		if request.user.is_authenticated:
			file=request.FILES['file']
			if file.name.endswith('.csv') == False:
					messages.error(request,'Files must be in .csv format to upload')
					return render(request,'website/uploads.html',context)

			form=FileForm(request.POST,request.FILES)

			if form.is_valid():
				print('formvalid')
				file = form.save(commit=False)
				file.user=request.user				
				file.save()
				messages.success(request, "Uploaded successfully")

			else:
				messages.error(request,'Submission not valid')
				print(form.errors)
				

		else:
			messages.error(request,'You must be logged in to upload files')
			

	
	return render(request,'website/uploads.html',context)




def download_file(request):
	if request.method =='GET':
		if request.user.is_authenticated:
			context={
					 'uploads':Uploads.objects.all()}
		else:
			messages.error(request,'You must be logged in to download files')
			context={}
	return render(request,'website/download.html',context)