#!/usr/bin/env python3
from urllib.parse import urljoin
import requests

NSW_DATA_PORTAL_BASE = "https://data.nsw.gov.au"
NSW_DATA_PORTAL_PATH = "data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29"

r = requests.get(urljoin(NSW_DATA_PORTAL_BASE, NSW_DATA_PORTAL_PATH), params={
  "limit"   : 100,
  "offset"  : 0,
})

data = r.json().get('result', {})

records = data.get('records',[])


while len(records) < int(data.get('total')):
  next = data.get('_links',{}).get('next',{})
  u = urljoin(NSW_DATA_PORTAL_BASE, f'/data{next}')
  r = requests.get(u)
  data = r.json().get('result', {})
  records.extend(data.get('records',[]))

records.sort(key=lambda v: v.get('notification_date'))

