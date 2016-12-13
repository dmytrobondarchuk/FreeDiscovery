"""
Duplicate Detection Example [REST API]
--------------------------------------

Find near-duplicates in a text collection
"""
from __future__ import print_function

from time import time
import sys
import platform
from itertools import groupby

import numpy as np
import pandas as pd
import requests
import sys

pd.options.display.float_format = '{:,.3f}'.format


dataset_name = "fedora_ml_3k_subset"     # see list of available datasets

BASE_URL = "http://localhost:5001/api/v0"  # FreeDiscovery server URL

print(" 0. Load the test dataset")
url = BASE_URL + '/datasets/{}'.format(dataset_name)
print(" GET", url)
res = requests.get(url)
res = res.json()

# To use a custom dataset, simply specify the following variables
data_dir = res['data_dir']

print("\n1.a Parse emails")
url = BASE_URL + '/email-parser'
print(" POST", url)
fe_opts = {'data_dir': data_dir }
res = requests.post(url, json=fe_opts)

dsid = res.json()['id']
print("   => received {}".format(list(res.json().keys())))
print("   => dsid = {}".format(dsid))



print("\n1.b. check the parameters of the emails")
url = BASE_URL + '/email-parser/{}'.format(dsid)
print(' GET', url)
res = requests.get(url)

data = res.json()
print('\n'.join(['     - {}: {}'.format(key, val) for key, val in data.items() \
                                                        if key != 'filenames']))

print("\n2. Email threading")

url = BASE_URL + '/email-threading/'
print(" POST", url)
t0 = time()
res = requests.post(url,
        json={'dataset_id': dsid }).json()

mid  = res['id']
print("     => model id = {}".format(mid))


def print_thread(container, depth=0):
    print(''.join(['> ' * depth,  container['subject'],
                   ' (id={})'.format(container['id'])]))

    for child in container['children']:
        print_thread(child, depth + 1)


print("\nThreading examples\n"
      "cf. https://www.redhat.com/archives/rhl-devel-list/2008-October/thread.htlm \n"
      "for ground truth data (mailman has a maximum threading depth of 3)"
       )
for idx in [5, 6, 7]:
    print(' ')
    print_thread(res['data'][idx])
