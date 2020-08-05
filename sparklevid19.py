import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# function to query Scottish Gov statistics website and get results back in json format
def sparql_query(url,query):
  r = requests.get(url, params = {'format': 'json', 'query': query})
  data = r.json()
  return data["results"]["bindings"]

# url should always be the same, query can be changed to get different data - gov website has a guide
url = 'http://statistics.gov.scot/sparql'
query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?periodname ?count
WHERE { 
  ?s <http://purl.org/linked-data/cube#dataSet> <http://statistics.gov.scot/data/coronavirus-covid-19-management-information> .
  ?s <http://purl.org/linked-data/sdmx/2009/attribute#unitMeasure> <http://statistics.gov.scot/def/concept/measure-units/testing-daily-people-found-positive>.
  ?s <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?perioduri.
  ?s <http://statistics.gov.scot/def/measure-properties/count> ?count.
  ?perioduri rdfs:label ?periodname.
} 
LIMIT 200
"""

# run query and get results
results = sparql_query(url,query)

# loop through query results and store dates and cases in lists
cases = []
date = []
for result in results:
  cases.append(int(result["count"]["value"]))
  date_str = result["periodname"]["value"]
  date_str = datetime.strptime(date_str,"%Y-%m-%d")
  date.append(date_str)

# use pandas to put data in a time series format, easier to plot this way
ts = pd.Series(cases,date)

# use matplotlib to plot the data
ts.plot()
plt.title("Scotland Daily Coronavirus Cases")
plt.ylabel("Infections")
plt.show()
