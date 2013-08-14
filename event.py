#!/usr/bin/env python

import sys
import urllib
import vgmdb.event
import json

def parse_event(event):
	url = 'http://vgmdb.net/event/%s?perpage=9999'%event
	data = vgmdb.event.fetch_event_page(url)
	event_info = vgmdb.event.parse_event_page(data)
	return json.dumps(event_info, sort_keys=True, indent=4, separators=(',',': '), ensure_ascii=False)
if __name__ == '__main__' and len(sys.argv) > 1:
	print parse_event(sys.argv[1]).encode('utf-8')
