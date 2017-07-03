#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from bs4 import BeautifulSoup
from json_mark import JsonMarker
from request_object import RequestObject
#from json_mark import JsonMarker


class RequestMarker:
    # TODO: отмечать параметры запросах REST стиля
    def __init__(self, request, injectionMark='§ §'):
        """Создает экзепляр класса RequestAnalyzer
        :param request: строка, содержащая сырой валидный запрос к серверу (например запросы из burpsuite)
        :param injectionMark: символы, разделенные пробелом, помечающие точки инъекции
        """
        self.injectionMark = injectionMark
        self.index_mark = 0
        self.excluded_headers = {'Host'}  # Если можно будет указывать, какие параметры пропускать
        self.all_headers = set()  # Все имена распарсенных хидеров будут здесь
        # Хидеры, которые будут добавлены в запрос, если их в нем нет
        self.extra_headers = {
            'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'X-Forwarded-For': '127.0.0.1',
            'X-Forwarded-Host': 'localhost'
        }

        self.request_object = RequestObject(request)

        self._markRequest()

    def getMarkedRequest(self):
        return self.request_object.market_request

    def getInitialRequest(self):
        return self.request_object.raw_request

    def _markRequest(self):
        """Помечает отдельные участки запроса и собирает их вместе в self.request_object.market_request"""
        self._markQueryString()
        self._markHeaders()
        self._markData()
	
        data = self.request_object.data
        if data == None:
                data = ""
        self.request_object.market_request = '\r\n'.join(
                [self.request_object.query_string] + self.request_object.headers) + '\r\n\r\n' + data
        print(self.request_object.market_request)

    def _markQueryString(self):
        """Помечает значения в строке запроса"""
        method, uri, http_ver = self.request_object.query_string.split(' ')

        uri = self._markByRegexp(uri, '=([^&]+)')
        uri = self._markEmptyParams(uri)

        self.request_object.query_string = ' '.join([method, uri, http_ver])
  
    def _markHeaders(self):
        """Помечает значения в хидерах"""
        modified_headers = []

        for header in self.request_object.headers:
            try:
                name, value = header.split(': ')
                self.all_headers.add(name)

                if name not in self.excluded_headers:
                    # Эвристика
                    if (' ' not in value) or (';' not in value and '=' not in value) \
                            or (';' in value and '=' not in value):
                        value = self.injectionMark.replace(' ', value) #  + ':' +  str(self.index_mark)
                    else:
                        value = self._markByRegexp(value, '=([^\s;]+);?') # + ':' +  str(self.index_mark)

            except ValueError as ve:
                print('[!] Exception in _markHeaders. Message: {}'.format(ve))

            modified_headers.append(': '.join([name, value]))

        for header, value in self.extra_headers.items():
            if header not in self.all_headers:
                modified_headers.append(': '.join([header, self.injectionMark.replace(' ', value)]))

        self.request_object.headers = modified_headers

    def _markData(self):
        """Помечает параметры в данных"""
        if not self.request_object.data:
            return

        content_type = self.request_object.content_type

        if content_type == 'json':
            self._markDataJson()
        elif content_type == 'xml':
            self._markDataXml()
        elif content_type == 'plain':
            self._markDataPlain()


    def _markDataPlain(self):
        """Помечаются данные вида param1=value1&param2=value2"""
        self.request_object.data = self._markByRegexp(self.request_object.data, '=([^&]+)')
        self.request_object.data = self._markEmptyParams(self.request_object.data)

    def _markDataJson(self):
        """Помечаются данные, представленные json"""
        json_encoder = JsonMarker(self.injectionMark)
        data = self.request_object.data

        data = json.loads(data)
        self.request_object.data = json_encoder.encode(data)

    def _markDataXml(self):
        """Помечаются данные, представленные xml"""
        # some kostyl
        attr_regexp1 = '''(^version|^encoding)="(.+?)"'''
        attr_regexp2 = '''='(.+?)\''''
        item_regexp = '''<[^\/]+?>([^\<\>]+?)<\/.+?>'''
        data = self.request_object.data

        data = self._markByRegexp(data, attr_regexp1)
        data = self._markByRegexp(data, attr_regexp2)
        data = self._markByRegexp(data, item_regexp)
        self.request_object.data = data

    def _markByRegexp(self, string, regexp, prefix='', group=1, flags=0):
        """Помечает параметры в строке по regexp'у
        :param string: Строка, в которой помечаются параметры
        :param regexp: Регулярное выражение, по которому они ищутся
        :param prefix: Префикс строки, на которую заменяется найденная группа
        :return: Измененная строка string
        """
        string = re.sub(regexp,
                        lambda x: prefix + x.group(0).replace(x.group(group),
                                                              self.injectionMark.replace(' ', x.group(group))),
                        string, flags=flags)
        return string

    def _markEmptyParams(self, string):
        """Помечает пустые параметры
        :param string: Строка, в которой пустые параметры ищутся
        :return: Измененная строка string
        """
        return re.sub('=(&|$)', lambda x: '=' + self.injectionMark + ('&' if '&' in x.group() else ''), string)





