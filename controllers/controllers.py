# -*- coding: utf-8 -*-
import babel.messages.pofile
import base64
import copy
import datetime
import functools
import glob
import hashlib
import io
import itertools
import jinja2
import json
import logging
import operator
import os
import re
import sys
import tempfile
import time

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from collections import OrderedDict, defaultdict, Counter
from werkzeug.urls import url_decode, iri_to_uri
from lxml import etree
import unicodedata

import odoo
import odoo.modules.registry
from odoo.api import call_kw, Environment
from odoo.modules import get_module_path, get_resource_path
from odoo.tools import image_process, topological_sort, html_escape, pycompat, ustr, apply_inheritance_specs, lazy_property
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.translate import _
from odoo.tools.misc import str2bool, xlsxwriter, file_open
from odoo.tools.safe_eval import safe_eval
from odoo import http, tools
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception, Response
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.models import check_method_name
from odoo.service import db, security

_logger = logging.getLogger(__name__)

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

	@http.route('/web/app', type='http', auth="none", sitemap=False)
	def web_login(self, redirect=None, **kw):
		ensure_db()
		request.params['login_success'] = False
		if request.httprequest.method == 'GET' and redirect and request.session.uid:
			return http.redirect_with_hash(redirect)

		if not request.uid:
			request.uid = odoo.SUPERUSER_ID

		values = request.params.copy()
		try:
			values['databases'] = http.db_list()
		except odoo.exceptions.AccessDenied:
			values['databases'] = None

		if request.httprequest.method == 'GET':
			old_uid = request.uid
			try:
				uid = request.session.authenticate(request.params['db'], request.params['login'], request.params['password'])
				request.params['login_success'] = True
				if request.params['debug'] == 'true':
					_logger.info('Connection from OdooApp [debug mode]')
					return http.redirect_with_hash(self._login_redirect_debug(uid, redirect=redirect))
				else:
					_logger.info('Connection from OdooApp')
					return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
			except odoo.exceptions.AccessDenied as e:
				request.uid = old_uid
				if e.args == odoo.exceptions.AccessDenied().args:
					values['error'] = _("Wrong login/password")
				else:
					values['error'] = e.args[0]
		else:
			if 'error' in request.params and request.params.get('error') == 'access':
				values['error'] = _('Only employee can access this database. Please contact the administrator.')

		if 'login' not in values and request.session.get('auth_login'):
			values['login'] = request.session.get('auth_login')

		if not odoo.tools.config['list_db']:
			values['disable_database_manager'] = True

		# otherwise no real way to test debug mode in template as ?debug =>
		# values['debug'] = '' but that's also the fallback value when
		# missing variables in qweb
		if 'debug' in values:
			values['debug'] = True

		response = request.render('web.login', values)
		#response.headers['X-Frame-Options'] = 'DENY'
		return response

	def _login_redirect(self, uid, redirect=None):
		return redirect if redirect else '/web'

	def _login_redirect_debug(self, uid, redirect=None):
		return redirect if redirect else '/web?debug#'
