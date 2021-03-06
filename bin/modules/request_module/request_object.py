#! /usr/bin/env python
# -*- coding: utf-8 -*-

class RequestObject:
    def __init__(self, request):
        self.raw_request = request
        self.market_request = ''

        self.query_string = ''
        self.headers = ''
        self.content_type = 'plain'
        self.data = ''
        self.known_types = {'text': {'html': 'plain', 'plain': 'plain', 'xml': 'xml'},
                            'application': {'atom+xml': 'xml', 'json': 'json', 'soap+xml': 'xml', 'xhtml+xml': 'xml',
                                            'xml-dtd': 'xml', 'xop+xml': 'xml', 'xml': 'xml'}}

        self._parse_request(self.raw_request)

    def _parse_request(self, raw_request):
        """ Распаковывает сырой запрос в объект"""
        # Разбиваем сырой запрос на 'строку запроса', 'хидеры' и 'дату'
        # на винде лажа с \r\n, остаются \n при считывании
        try:
            self.headers, self.data = raw_request.split('\n\n')
        except ValueError as ve:
            self.headers, self.data = raw_request, None

        self.query_string, self.headers = self.headers.split('\n')[0], [x for x in self.headers.split('\n')[1:] if x]

        self._identify_content_type()

    def _identify_content_type(self):
        """Находит хидер Content-type, парсит type и subtype и определяет по known_types форму данных"""
        content_type = next((header for header in self.headers if header.startswith('Content-Type')), None)

        if content_type:
            type, subtype = content_type.split(': ')[1].split('/')
            self.content_type = self.known_types.get(type).get(subtype)
