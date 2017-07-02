#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

def _delete_token(token, request):
    new = request.replace(token, "")
    return new

def _prepate_req(token, start, end, request, payload):
    request = request[:start] + payload + request[end + 1:]
    return _delete_token(token, request)


def get_requests_with_payloads(request, payload):
#    print(request)

    result = []
    token = '§'
    state = 2
    start = 0
    end = 0

    for i,ch in enumerate(request):
        if (token == ch) and (state == 2) :
            state = 1
            start = i
        elif (token == ch) and (state == 1):
            end = i
            state = 2
            result.append(_prepate_req(token, start, end, request, payload))
    return result
