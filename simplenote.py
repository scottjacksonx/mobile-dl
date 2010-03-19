#!/usr/bin/env python

import base64
import datetime
import logging
import urllib
import urllib2

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

USER_AGENT = "python-simplenote/0.1"

class SimplenoteError(Exception):
    def __init__(self, method, msg):
        self.method = method
        self.msg = msg

    def __repr__(self):
        return "%s: [%s] %r" % (self.__class__.__name__, self.method, self.msg)

class SimplenoteAuthError(SimplenoteError):
    def __init__(self, email, msg):
        self.email = email
        self.method = "auth"
        self.msg = msg

class Simplenote(object):
    api_url = "https://simple-note.appspot.com/api/"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._get_token()

    def _get_token(self):
        if hasattr(self, '_token'):
            return self._token

        url = self.api_url + 'login'

        form_fields = {
            'email': self.email,
            'password': self.password
        }
        data = base64.b64encode(urllib.urlencode(form_fields))

        try:
            res = urllib2.urlopen(urllib2.Request(
                url = url,
                data = data,
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': USER_AGENT,
                }))
        except urllib2.HTTPError, exc:
            raise SimplenoteAuthError(self.email, repr(exc))

        if res.getcode() != 200:
            raise SimplenoteAuthError(email, "Request failed with response %d" % res.getcode())

        self._token = res.read().strip()
        return self._token

    def _set_token(self, token):
        self._token = token

    token = property(_get_token, _set_token)

    def _query(self, action, isjson=True, post=None, **kwargs):
        kwargs['auth'] = self.token
        kwargs['email'] = self.email
        args = urllib.urlencode(kwargs)
        url = "%s%s?%s" % (self.api_url, action, args)

        headers = {'User-Agent': USER_AGENT}

        if post:
            if isinstance(post, unicode):
                post = post.encode('utf-8')
            data = base64.b64encode(post)
            req = urllib2.Request(url=url, data=data, headers=headers)
        else:
            req = urllib2.Request(url=url, headers=headers)

        try:
            res = urllib2.urlopen(req)
        except urllib2.HTTPError, exc:
            raise SimplenoteError(action, repr(exc))

        if res.getcode() != 200:
            raise SimplenoteError(action, "Request failed with response %d" % res.getcode())

        if isjson:
            return json.loads(res.read().replace('\t', '\\t'))

        return res

    def _parse_datetime(self, val):
        return datetime.datetime.strptime(val.split('.', 1)[0], "%Y-%m-%d %H:%M:%S")

    def index(self):
        notes = self._query("index")
        for n in notes:
            n['modify'] = self._parse_datetime(n['modify'])
        return notes

    def search(self, query, max_results=10, offset=0):
        results = self._query("search", query=query, results=max_results, offset=offset)
        return dict(
            total_records = results['Response']['totalRecords'],
            results = results['Response']['Results'],
        )

    def get_note(self, key):
        res = self._query("note", isjson=False, key=key)
        return dict(
            content = res.read(),
            key = key,
            modified = self._parse_datetime(res.headers['note-modifydate']),
            created = self._parse_datetime(res.headers['note-createdate']),
        )

    def update_note(self, key, content):
        res = self._query("note", isjson=False, post=content, key=key)
        return res.read().strip()

    def create_note(self, content):
        res = self._query("note", isjson=False, post=content)
        return res.read().strip()

    def delete_note(self, key):
        self._query("delete", key=key, isjson=False)
        return True
