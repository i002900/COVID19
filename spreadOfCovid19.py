
import pandas as pd
import folium  #for graphing
from folium.plugins import TimestampedGeoJson
import webbrowser as wb


## John Hopkins Data Set
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
# Read CSV file from URL
cases_df = pd.read_csv(url , index_col = 0)
# The Columns are organised as follows:
#
#Index Column: Province/State
#0. Country/Region
#1. Latitude
#2. Longitude
#3. column 3 onwards: Daily cumulative reported cases (by date)

# Determine First infection date for each entry and store it as a List
num_cols = len(cases_df.columns) + 1
firstInfectionDates = []
first_infection = ' '
i = 0
for idx , value in cases_df.iterrows():
    
    first_infection = ' '
    for i in range(3 , num_cols): #Date recordings from column 3 onwards - one column per date
       if value[i] > 0:
            first_infection = cases_df.columns[i]
            firstInfectionDates.append(first_infection)
            break # Capture first date recorded and leave
        
#Convert the List of Dates into a Series
Date = pd.Series(firstInfectionDates , name = 'Date')

# Convert Date to date/time format
Date = pd.to_datetime(Date, format='%m/%d/%y')

# Slice Data Frame and Combine with the Date series into a new data frame
cases1_df = cases_df[['Country/Region' , 'Lat', 'Long']]
Globalcases_df = pd.concat([cases1_df.reset_index(), Date], axis = 1 )

# Now sort by date to organise chronologically
Globalcases_df.sort_values(['Date'], inplace = True)

#Extract Latitude,Longitude for dropping markers
Mapdata = [[value.Date , value.Lat, value.Long] for idx , value in Globalcases_df.iterrows()]
LatMean =  Globalcases_df.Lat.mean()
LongMean = Globalcases_df.Long.mean()

# Build features array for use with GeoJson
features = []
for idx, value in Globalcases_df.iterrows():
    times = str(value.Date)
    times = times[:10]        #YYYY-MM-DD
    feature = {
            'type': 'Feature',
            'geometry': {
                'type':'Point', 
                'coordinates':[value.Long,value.Lat]  #GeoJson Coordinates are Longitude, Latitude, Altitude!
            },
            'properties': {
                'time': times,
                'icon': 'circle',
                'iconstyle':{
                    'fillOpacity': 0.8,
                    'color': 'red',
                    'stroke': 'true',
                    'radius': 3,
                   
                }
            }
        }
    features.append(feature)

VirusMap = folium.Map(location=[LatMean , LongMean ], tiles='StamenTerrain', zoom_start=2.5)
            
        
TimestampedGeoJson(
        {'type': 'FeatureCollection',
        'features': features}
        , period='P1D'
        , add_last_point=False
        , auto_play=True
        , loop=True
        , max_speed=1
        , loop_button=True
        , date_options='YYYY-MM-DD'
        , time_slider_drag_update=True
        
    ).add_to(VirusMap)

VirusMap.save('PandemicSpread.html')

wb.open('PandemicSpread.html', new=2)


                            
        
    

