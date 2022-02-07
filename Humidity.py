'''
API_key
#  your API key --> https://opendata.aemet.es/centrodedescargas/inicio

Example links:
Prediccion Horaria
url = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/41013/'

'''

import requests
import time
import pandas as pd

'''
This is a standard request for opendata.aemet.es/opendata/api/ 
initial response return a json with the following
{
  "descripcion" : "exito",
  "estado" : 200,
  "datos" : "https://opendata.aemet.es/opendata/sh/EXAMPLE",
  "metadatos" : "https://opendata.aemet.es/opendata/sh/93a7c63d"
}
with data at 
  "datos" : "https://opendata.aemet.es/opendata/sh/EXAMPLE"

Full report is returned as a json
'''
def opendata_req(url, API_key):
    querystring = {'api_key': API_key}
    headers = {
                'cache-control': 'no-cache'
              }

    response = requests.request('GET', url, headers=headers, params=querystring)
    data_url = response.json()

    response = requests.get(data_url['datos'])
    report   = response.json()


    return report

'''
This function return a dict with Hourly Humidity prediction for a particular location, like the following,
{'Humidity': ['92', '79', '72', '66', '54', '48', '41', '35', '31', '32', '37', '40', '41', '39', '41', '43'], 
 'Time':     ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']}

And time of the prediction request,
2022-02-07T16:26:08
'''

def get_Humidity_Hourly(url,API_key):

    meteo_report  = []
    Humidity_report = {'Humidity' : [], 'Time' : [] }

    req_report = opendata_req(url, API_key)
    req_time   = req_report[0]['elaborado']
    print(req_time)

    if meteo_report == []:
        meteo_report.append(req_report)

        for d in range(0,len(meteo_report[0][0]['prediccion']['dia'][0]['humedadRelativa'])):
                Humidity_report['Humidity'].append(meteo_report[0][0]['prediccion']['dia'][0]['humedadRelativa'][d]['value'])
                Humidity_report['Time'].append(meteo_report[0][0]['prediccion']['dia'][0]['humedadRelativa'][d]['periodo'])
    
    return Humidity_report, req_time



'''
Input values  for the following API call
'''
url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/41013/"
API_key =  '' # your API key --> https://opendata.aemet.es/centrodedescargas/inicio


'''
API call for Humidity Hourly prediction as location defined by url
'''
Humidity_Hourly, req_time = get_Humidity_Hourly(url,API_key)

#print(Humidity_Hourly)
print(req_time)

'''
Save as .csv
'''
Humidity_Hourly_df = pd.DataFrame(Humidity_Hourly)
Humidity_Hourly_df.to_csv(str(req_time).replace(' ', '').replace(':', '').replace('-','') 
        + '_hourly.csv', index = None, header=True)