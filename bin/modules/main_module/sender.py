#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import socket
import urllib
import httplib2
import json
import modules.main_module.common as common
import modules.analyser_module.analyser as analyser

def send(request, payloads, config):
	with open(payloads) as f:
		for payload in f.readlines():
			payl = urllib.parse.quote(payload.replace('\n', ''))	
			res = common.get_requests_with_payloads(request, payl)
			_send(res, config)
			#print(res)
	
def _sendRequestThread(request, config):
	print(request)
	host = _parseRequest(request).rstrip()
	splitReq = request.splitlines()
	firstLine = list(filter(None, splitReq[0].split(' ')))
	method = firstLine[0]
	path = firstLine[1]
	headers = {}
	params = ""
	uri = ''	
	isData = False
	for header in splitReq[1:]:

		if header == '' or header == "\n":
			isData = True
			continue
		
		if isData: 
			params += header
			continue	
		
		headerSplit = header.split(':', 1)
		name = headerSplit[0]
		value = headerSplit[1]
		headers[name] = value
	
	params = urllib.parse.quote_plus(params)	
	
	if config["IS_SSL"]:
		uri = 'https://' + host + path 
	else:
		uri = 'http://' + host + path	
	
	http = httplib2.Http()
	response,content = http.request(uri, method, headers=headers, body=params)
	
	analyser.analyseResponse(response)
	analyser.analyseContent(content)

# TODO: SSL cipher
def _send(requests, config):
	for request in requests:
		_sendRequestThread(request, config)

def _parseRequest(request):
	regex = re.search(r'Host:[\s]*(.*)', request).group(1)
	return regex
