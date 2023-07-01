# -*- coding: utf-8 -*-
"""CS66_final_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MWu1RtbRzPFsfcrF_b8s9_D6_Fr4ios_
"""

#spencer french and gabe meier - CS66 Final project - netflix data analysis
#imports
import pandas as pd
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go


def mergeSortData(adict, parameter):
    #print("Splitting ",alist)
    if len(adict)>1:
        mid = len(adict)//2
        lefthalf = adict[:mid]
        righthalf = adict[mid:]

        mergeSortData(lefthalf, parameter)
        mergeSortData(righthalf, parameter)

        i=0
        j=0
        k=0
        #merging the two lists
        #i and j are indices of left and right lists
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][parameter] >= righthalf[j][parameter]:
                adict[k]=lefthalf[i]
                i=i+1
            else:
                adict[k]=righthalf[j]
                j=j+1
            # k is the index in the 'result' list
            k=k+1

        #once we're done with the above, we may have items left over in one of the lists
        #so, one of these two while loops will run (but not both)
        while i < len(lefthalf):
            adict[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            adict[k]=righthalf[j]
            j=j+1
            k=k+1
    #print("Merging ",alist)


df = pd.read_csv('ViewingActivity.csv')



#formatting the table
df = df.drop(['Bookmark', 'Latest Bookmark', 'Country','Device Type'], axis=1)

#formatting the start time variable
df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
df = df.set_index('Start Time')
df.index = df.index.tz_convert('US/Central')
df = df.reset_index()
df.head(1)

#formatting the duaration variable
df['Duration'] = pd.to_timedelta(df['Duration'])
df.dtypes

#getting rid of the episode titles
for i in range(len(df)):
  df.at[i, 'Title']= df['Title'].loc[df.index[i]].split(":")[0]


#bar graph for shows

def total_show_watchtime_all():
  #empty list for every single episode and movie and how long we spent watching it
  list_ofshows=[]
  for i in range(len(df)):
    #iterate through every entry, filter out anything thats not a full episode or movie
    if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP':
      showinfor= {"Duration":df.loc[i,'Duration'],"Title":df.loc[i,'Title']}
      list_ofshows.append(showinfor)
  #dictionary to hold show name and it's total duration
  dict_totals = {}

  for i in range(len(list_ofshows)):
    #if show isn't in dictionary yet add it to the diction
    if list_ofshows[i]["Title"] not in dict_totals:
      dict_totals[list_ofshows[i]["Title"]] = list_ofshows[i]["Duration"]
    #if the show is already in the dictionary add the duration from this episode to the show's total duration
    else:
      dict_totals[list_ofshows[i]["Title"]] += list_ofshows[i]["Duration"]

  totals = []
  for key in dict_totals:
    #change format of dictionary to a list of dictionaries
    totals.append({"Title":key,"Total Duration":dict_totals[key]})

  #Sort the data
  mergeSortData(totals,"Total Duration")
  shows = []
  total_durations = []
  #Make a list of top 10 shows and a corresponding list of their total watchtime
  for i in range(10):
    shows.insert(0,totals[i]["Title"])
    #makes the total duration variable the amount of days it was watched for
    total_durations.insert(0,totals[i]["Total Duration"].total_seconds()/(3600*24))
  #Creating the graph
  fig = px.bar(x=shows,y=total_durations,title ='Most Watched Shows by Total Watch Time')
  fig.update_layout(
    xaxis_title="Show",
    yaxis_title="Days",
    )
  fig.show()

#Same as function above but it is specific to one user
def total_show_watchtime_user(user):
  list_ofshows=[]
  for i in range(len(df)):
    if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP' and df.loc[i,'Profile Name'] == user:
      showinfor= {"Duration":df.loc[i,'Duration'],"Title":df.loc[i,'Title']}
      list_ofshows.append(showinfor)

  dict_totals = {}

  for i in range(len(list_ofshows)):
    if list_ofshows[i]["Title"] not in dict_totals:
      dict_totals[list_ofshows[i]["Title"]] = list_ofshows[i]["Duration"]
    else:
      dict_totals[list_ofshows[i]["Title"]] += list_ofshows[i]["Duration"]

  totals = []
  for key in dict_totals:
    totals.append({"Title":key,"Total Duration":dict_totals[key]})


  mergeSortData(totals,"Total Duration")
  shows = []
  total_durations = []
  for i in range(10):
    shows.insert(0,totals[i]["Title"])
    total_durations.insert(0,totals[i]["Total Duration"].total_seconds()/(3600*24))
  fig = px.bar(x=shows,y=total_durations,title =str(user)+"'s Most Watched Shows by Total Watch Time")
  fig.show()

#pie chart for user duration
def user_watchtime_piechart():
  #filter out unwanted video types
  list_ofshows2=[]
  for i in range(len(df)):
    if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP':
      showinfor2= {"Duration":df.loc[i,'Duration'],"User":df.loc[i,'Profile Name']}
      list_ofshows2.append(showinfor2)
  #dictionary for total watchtime of every profile
  dict_totals2 = {}

  for i in range(len(list_ofshows2)):
    #adds a profile to the dictionary if it's not there yet
    if list_ofshows2[i]["User"] not in dict_totals2:
      dict_totals2[list_ofshows2[i]["User"]] = list_ofshows2[i]["Duration"]
    #adds the duration of the episode to the profile is it was already there
    else:
      dict_totals2[list_ofshows2[i]["User"]] += list_ofshows2[i]["Duration"]
  #change dictionary into a list of dictionaries
  user_totals = []
  for key in dict_totals2:
    user_totals.append({"Title":key,"Total Duration":dict_totals2[key]})
  labels = []
  sizes = []
  #Makes the list of dictionaries into a list of profiles and corresponding total duration
  for i in range(len(user_totals)):
    labels.append(user_totals[i]['Title'])
    sizes.append(user_totals[i]['Total Duration'].total_seconds())
  #Create the chart
  fig = go.Figure(data=[go.Pie(labels=labels, values=sizes,title="Percentage of Total Watch Time Per Profile")])
  fig.update_layout(
    xaxis_title="show",
    yaxis_title="Days",
    )
  fig.show()

#time of day that you start episodes, can be with one or all profiles/shows
def time_of_day(show="all shows",user=0):
  start_times=[]
  #filter out the unwanted video types and the unwanted shows/profiles
  #add the hour parameter of the start time so we know the hour of the day it was started
  for i in range(len(df)):
    if show=='all shows':
      if user == 0:
        if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP' and df.loc[i,"Duration"].total_seconds()>300:
          start_times.append(df.loc[i,'Start Time'].hour)
      else:
        if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP' and df.loc[i,"Duration"].total_seconds()>300 and df.loc[i,"Profile Name"] == user:
          start_times.append(df.loc[i,'Start Time'].hour)
    else:
      if user == 0:
        if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP' and df.loc[i,'Title']==show and df.loc[i,"Duration"].total_seconds()>300:
          start_times.append(df.loc[i,'Start Time'].hour)
      else:
        if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP' and df.loc[i,'Title']==show and df.loc[i,"Duration"].total_seconds()>300 and df.loc[i,"Profile Name"] == user:
          start_times.append(df.loc[i,'Start Time'].hour)
  #list will countain the amount of episodes started at each time
  #counter[13] will correspond to shows started at 1:00pm
  counter = [0]*24
  for times in start_times:
    counter[times] += 1
  #list of times of days that corresponds to the values in counter
  times_of_day = ["12 a.m.","1 a.m.","2 a.m.","3 a.m.","4 a.m.","5 a.m.","6 a.m.","7 a.m.","8 a.m.","9 a.m.","10 a.m.","11 a.m.","12 p.m.","1 p.m.","2 p.m.","3 p.m.","4 p.m.","5 p.m.","6 p.m.","7 p.m.","8 p.m.","9 p.m.","10 p.m.","11 p.m."]
  #create graph
  fig = px.bar(x=times_of_day,y=counter,title="Amount of episodes of "+show+" started by time of day")
  fig.update_layout(
    xaxis_title="Time of day",
    yaxis_title="Episodes Started",
    #yaxis_range=[2013, None]
  )
  fig.show()

#function to choose a show to make the time of day distribution from
def choose_show_for_time_dist(user=0):
  list_ofshows=[]
  #basically the same code as the top shows function
  for i in range(len(df)):
    if user==0:
      if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP':
        showinfor= {"Duration":df.loc[i,'Duration'],"Title":df.loc[i,'Title']}
        list_ofshows.append(showinfor)
    else:
      if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP' and df.loc[i,'Profile Name'] == user:
        showinfor= {"Duration":df.loc[i,'Duration'],"Title":df.loc[i,'Title']}
        list_ofshows.append(showinfor)

  dict_totals = {}

  for i in range(len(list_ofshows)):
    if list_ofshows[i]["Title"] not in dict_totals:
      dict_totals[list_ofshows[i]["Title"]] = list_ofshows[i]["Duration"]
    else:
      dict_totals[list_ofshows[i]["Title"]] += list_ofshows[i]["Duration"]

  totals = []
  for key in dict_totals:
    totals.append({"Title":key,"Total Duration":dict_totals[key]})


  mergeSortData(totals,"Total Duration")
  #make one string that lists the top ten shows for the user so they have ideas of what they can see the distribution for
  top_ten = ""
  for i in range(10):
    top_ten+=(totals[i]["Title"])
    if i<9:
      top_ten+= ", "
  print("Top Ten shows: "+top_ten)
  choice = input("Choose a show from the list above")
  #calls the time of day function with the user specified parameters
  time_of_day(choice,user)

#bar graph of total watchime by year
def bars_by_year():
    #reformatting the data
    df2 = pd.read_csv('ViewingActivity.csv')
    #formatting the table
    df2= df2.drop(['Bookmark', 'Latest Bookmark', 'Country'], axis=1)
    df2['Duration'] = pd.to_timedelta(df['Duration'])
    #Make the starttime field only include the year that the episode was started in
    for i in range(len(df2)):
        df2.at[i, 'Start Time']= str(df['Start Time'].loc[df.index[i]]).split("-")[0]
    list_ofshows2=[]
    #filter out unwanted video types
    for i in range(len(df2)):
        if df2.loc[i,'Supplemental Video Type'] != 'HOOK'and df2.loc[i,'Supplemental Video Type'] != 'TRAILER' and df2.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df2.loc[i,'Supplemental Video Type'] != 'RECAP':
            showinfor2= {"Duration":df2.loc[i,'Duration'],"Year":df2.loc[i,'Start Time']}
            list_ofshows2.append(showinfor2)
    #dictionary of all the different years and their total time
    dict_totals2 = {}
    for i in range(len(list_ofshows2)):
        #if a year isn't in the dictionary yet, add it
        if list_ofshows2[i]["Year"] not in dict_totals2:
            dict_totals2[list_ofshows2[i]["Year"]] = list_ofshows2[i]["Duration"]
        #if it is already in the dictionary add the watchtime of that one episode to the total time for that year
        else:
            dict_totals2[list_ofshows2[i]["Year"]] += list_ofshows2[i]["Duration"]
    user_totals = []
    #change the dictionary into a list of dictionaries
    for key in dict_totals2:
        user_totals.append({"Year":key,"Total Duration":dict_totals2[key]})
    labels=[]
    sizes=[]
    #change the list of dictionaries into two corresponding lists
    for i in range(len(user_totals)):
        labels.append(int(user_totals[i]['Year']))
        sizes.append(user_totals[i]['Total Duration'].total_seconds()/86400)
    #Create the graph
    fig = px.bar(x=labels,y=sizes,title="Total Watch Time by Year")
    fig.update_layout(
      xaxis_title="Years",
      yaxis_title="Days",
      yaxis_range=[2013, None]
    )
    fig.show()
def list_names():
  profile_list=[]
  list_ofshows2=[]
  for i in range(len(df)):
    if df.loc[i,'Supplemental Video Type'] != 'HOOK'and df.loc[i,'Supplemental Video Type'] != 'TRAILER' and df.loc[i,'Supplemental Video Type'] != 'TEASER_TRAILER' and df.loc[i,'Supplemental Video Type'] != 'RECAP':
      showinfor2= {"Duration":df.loc[i,'Duration'],"User":df.loc[i,'Profile Name']}
      list_ofshows2.append(showinfor2)


  for i in range(len(list_ofshows2)):
    if list_ofshows2[i]["User"] not in profile_list:
      profile_list.append(list_ofshows2[i]["User"])

  return profile_list


def graph_presentation():
  input1=input("would you like look at our netflix statistics (Y/N):")
  if input1 == 'Y':
    print("what stats would you like to look at?")
    print("1.)Percentage of total duration by profile.")
    print("2.) How much netflix we watched per year")
    print("3.) What time of the day we usually watch netflix")
    print("4.) Our top watched shows of all time")
    input2=input("select the number of the query you want to see:")
    if input2 == '1':
      print("here is the data you requested")
      user_watchtime_piechart()
      graph_presentation()
    if input2 == '2':
      print("here is the data you requested")
      bars_by_year()
      graph_presentation()
    if input2 == '3':
      input3= input("would you like to look at all profiles or just one  ( type all or one):")
      if input3 == 'all':
        input4= input("would you like to look at all shows or just one  ( type all or one):")
        if input4 == 'all':
          print("here is the data you requested")
          time_of_day(show="all shows",user=0)
          graph_presentation()
        else:
          choose_show_for_time_dist(user=0)
          graph_presentation()
      else:
        print(list_names())
        print("select a name from the list above")
        input5= input()
        input6= input("would you like to look at all shows or just one  ( type all or one):")
        if input6 == 'all':
          print("here is the data you requested")
          time_of_day(show="all shows",user=input5)
          graph_presentation()
        else:
            print("here is the data you requested")
            choose_show_for_time_dist(user=input5)
            graph_presentation()
    if input2 == '4':
          input7= input("would you like to look at all profiles or just one  ( type all or one):")
          if input7 == 'all':
            print("here is the data you requested")
            total_show_watchtime_all()
            graph_presentation()
          else:
            print(list_names())
            print("select a name from the list above")
            input8= input()
            total_show_watchtime_user(input8)
            graph_presentation()
  else:
    print("thanks for watching our presentation")
    quit()

graph_presentation()
#Code from where we attempted to make it all work as a website with a dropdown menu