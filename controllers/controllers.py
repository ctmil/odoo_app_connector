# -*- coding: utf-8 -*-
import ast
import base64
import csv
import functools
import glob
import itertools
import jinja2
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import sys
import time
import urllib2
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
	import xlwt
except ImportError:
	xlwt = None

import openerp
import openerp.modules.registry
from openerp.addons.base.ir.ir_qweb import AssetsBundle, QWebTemplateNotFound
from openerp.tools import topological_sort
from openerp.tools.translate import _
from openerp.tools import ustr
from openerp import http
from openerp.http import request, serialize_exception as _serialize_exception

def ensure_db(redirect='/web/database/selector'):
	db = request.params.get('db') and request.params.get('db').strip()

	if db and db not in http.db_filter([db]):
		db = None

	if db and not request.session.db:
		r = request.httprequest
		url_redirect = werkzeug.urls.url_parse(r.base_url)
		if r.query_string:
			query_string = iri_to_uri(r.query_string)
			url_redirect = url_redirect.replace(query=query_string)
		request.session.db = db
		abort_and_redirect(url_redirect)

	if not db and request.session.db and http.db_filter([request.session.db]):
		db = request.session.db

	if not db:
		db = db_monodb(request.httprequest)

	if not db:
		werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))

	if db != request.session.db:
		request.session.logout()
		abort_and_redirect(request.httprequest.url)

	request.session.db = db

class OdooAppConnector(http.Controller):

	@http.route('/web/app', type='http', auth="none")
	def web_login_app(self, redirect=None, **kw):
		ensure_db()

		if request.httprequest.method == 'GET' and redirect and request.session.uid:
			return http.redirect_with_hash(redirect)

		if not request.uid:
			request.uid = openerp.SUPERUSER_ID

		values = request.params.copy()
		if not redirect:
			redirect = '/web?' + request.httprequest.query_string
		values['redirect'] = redirect

		try:
			values['databases'] = http.db_list()
		except openerp.exceptions.AccessDenied:
			values['databases'] = None

		if request.httprequest.method == 'GET':
			old_uid = request.uid
			uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
			if uid is not False:
				return http.redirect_with_hash(redirect)
			request.uid = old_uid
			values['error'] = _("Wrong login/password")
		if request.env.ref('web.login', False):
			return request.render('web.login', values)
		else:
			error = 'Unable to login on database %s' % request.session.db
			return werkzeug.utils.redirect('/web/database/selector?error=%s' % error, 303)
