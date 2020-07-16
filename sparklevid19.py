import requests
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
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()

results = data["results"]["bindings"]

infections = []
for result in results:
	infections.append({"date" : result["periodname"]["value"], "cases" : result["count"]["value"]})

import pandas as pd
df = pd.DataFrame(infections)
df.set_index('date', inplace=True)
#df = df.astype({'cases' : float)
df.head()
print(df)