import requests
import pandas as pd
import numpy as np

from time import sleep
def api_query(query: str, results=[], queries=1, max_queries=None) -> list:
    '''Recursively query the API, up to `max_queries`. (If `max_queries=None`, we
    will paginate through the results as long as they run).
    '''
    base_url = 'https://api.ooni.io/api/v1/'
    query = '{!s}{!s}'.format(base_url, query)

    try:
        resp = requests.get(query).json()
        results = results + resp['results']
        next_url = resp['metadata']['next_url']
        if max_queries is not None and queries > max_queries:
            return results
        if next_url:
            # sleep so as to not overwhelm the endpoint
            sleep(0.1)
            # remove base url to perfrom the query
            next_url = next_url.split('api/v1/')[1]
            return api_query(next_url, results, queries + 1, max_queries)
        return results
    except Exception as inst:
        # if we have an error,
        print("Error querying API: {!s}".format(inst))
        # just return what we've collected
        # (at worst, `results` will be `[]`)
        return results

BASE_QUERY = 'measurements?test_name=web_connectivity&anomaly=true&order_by=test_start_time&limit=1000&probe_cc=AZ'

def query_recent_measurements(max_queries=5) -> list:
    '''Queries all recent measurements, up to specified maximum number of queries.'''
    return api_query(BASE_QUERY, max_queries=max_queries)

results = query_recent_measurements()


def query_test_results(probe_cc, test_name, max_queries=5, limit = 1000):
    """ Queries and returns test results given country code and test name.
    Available values for test_name: bridge_reachability, dash, dns_consistency, dnscheck, 
    facebook_messenger, http_header_field_manipulation, http_host, http_invalid_request_line,
    http_requests, meek_fronted_requests_test, multi_protocol_traceroute, ndt, psiphon,
    riseupvpn, signal, tcp_connect, telegram, tor, torsf, urlgetter, vanilla_tor,
    web_connectivity, whatsapp.
    """
    BASE_QUERY = 'measurements?test_name=' + test_name
    BASE_QUERY += '&probe_cc=' + probe_cc + '&limit=' + str(limit)
    return api_query(BASE_QUERY, max_queries=max_queries)
    

test_results = query_test_results('US', 'web_connectivity')
test_results #[1]#['anomaly']




"""
    import pandas as pd
    country_code = []
    country_code.append(test_results[1]['test_name'])
    #country_code
    df = pd.DataFrame({ 'country_code': country_code})
    df
"""

def test_results_to_df(test_results):
  anomaly = []
  confirmed = []
  test_name = []
  country_code = []

  for i in np.arange(len(test_results)):
      anomaly.append(test_results[i]['anomaly'])
      confirmed.append(test_results[i]['confirmed'])
      test_name.append(test_results[i]['test_name'])
      country_code.append(test_results[i]['probe_cc'])
  #print(anomaly)

  df = pd.DataFrame({
                      'country_code': country_code,
                      'anomaly': anomaly,
                      'confirmed': confirmed,
                      'test_name': test_name
                       })
    
  return df

df = test_results_to_df(test_results)
df.head()

