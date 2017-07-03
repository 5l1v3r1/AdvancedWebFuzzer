#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import modules.main_module.sender as sender
import json

from modules.request_module.marker import RequestMarker

def createParams():
	params = argparse.ArgumentParser()
	params.add_argument ('request_file')
	params.add_argument ('payloads_file')
	params.add_argument ('--config', default='config.json')
	return params

def checkInput(params):
	if not os.path.exists(params.request_file):
		sys.stderr.write('ERROR: Path request file was not found!')
		return True

	if not os.path.exists(params.payloads_file):
		sys.stderr.write('ERROR: Path dictionary file was not found!')
		return True
	
	if not os.path.exists(params.config):
		sys.stderr.write('ERROR: Config file was not found!')
		return True
	

if __name__ == '__main__':
	params = createParams().parse_args()
	
	if checkInput(params):
		sys.exit(1)

	requestFile = params.request_file
	dictionaryFile = params.payloads_file

	with open(requestFile) as f:
		request_string = f.read()
	
	with open(params.config) as f2:	
		config = json.loads(f2.read())
		print(config)

	req = RequestMarker(request_string)
	mark_request = req.getMarkedRequest()
	sender.send(mark_request, dictionaryFile, config)
	



