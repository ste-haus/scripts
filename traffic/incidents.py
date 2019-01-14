#!/usr/bin/env python3

import json, os, urllib.request

directory = os.path.dirname(os.path.abspath(__file__))
credentials = json.load(open(directory + '/credentials.json'))

filters = 'incidents'

base_url = 'https://www.mapquestapi.com/traffic/v2/incidents'
url = '%s?key=%s&boundingBox=%s&filters=%s' % (base_url, credentials['api_key'], credentials['area'], filters)

response = None
with urllib.request.urlopen(url) as stream:
    sResponse = stream.read().decode('utf-8')
    response = json.loads(sResponse)

if response != None:
    incidents = []
    for incident in response['incidents']:
        road = incident['parameterizedDescription']['roadName']
        direction = incident['parameterizedDescription']['direction']

        if road in credentials['roads']:
            if incident['impacting']:
                incidents.append({
                    'road': road,
                    'direction': ('' if direction == 'None' else ' ' + direction),
                    'description': incident['fullDesc'],
                    'delay': int(incident['delayFromTypical'])
                })

print(json.dumps(incidents))