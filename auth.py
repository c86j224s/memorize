#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import uuid, json
import timehelper
from kvstore import KVStore

class UserAuthentication (object):
	#
	#	%email%_auth
	#
	#	{
	#		"pwdhash":,
	#		"pwdtype":,
	#		"confirmed":,
	#		"confirmcode":,
	#		...
	#	}
	#
	#	.tmp/%email%_%session%
	#
	#	{
	#		"expire" : (utc time),
	#		"sessionid" : $session$,
	#		...
	#	}
	#
	#	TODO need functionality to kick out sessions
	#
	def __init__ (self, conf):
		self.auth_postfix = "_auth"
		self.auth_store = KVStore.new (conf.get ("kvstore_type"), conf.get ("rootdir") + conf.get ("kvstore_location"))

		self.temp_store = KVStore.new (KVStore.LOCAL_STORE, conf.get ("rootdir") + "tmp", reset=True)
		self.pwdtype = conf.get ("pwdtype")
		self.expire_duration = conf.get ("expire_duration", 365*24*60*60)

	def sign_up (self, email, pwd):
		if len(pwd) == 0:
			return False	# no pwd

		if self._get_authinfo (email):
			return False	# already exist
		
		info = {}
		info["pwdhash"] = self._get_pwdhash (pwd)
		info["pwdtype"] = self.pwdtype
		info["confirmed"] = False
		info["confirmcode"] = None

		return self._set_authinfo (email, info)

	def sign_in (self, email, pwd):
		if len (pwd) == 0:
			return None		# no pwd

		info = self._get_authinfo (email)
		if not info:
			return None		# no matched user

		if not info.get ("confirmed"):
			return None		# not confirmed by email

		if info.get("pwdhash") != self._get_pwdhash (pwd, info.get ("pwdtype")):
			return None		# invalid pwd

		sessionid = self._new_sessionid ()
		sessioninfo = {}
		sessioninfo ["expire"] = timehelper.serializeDateTimeToDict (datetime.utcnow () + timedelta (self.expire_duration))
		sessioninfo ["sessionid"] = sessionid
		self._set_session (email, sessionid, sessioninfo)

		return sessionid

	def sign_out (self, email, sessionid):
		return self._del_session (email, sessionid)

	def change_password (self, email, old_pwd, new_pwd):
		if len (old_pwd) == 0 or len (new_pwd) == 0:
			return False	# no pwdhash

		if old_pwd == new_pwd:
			return False	# not changed pwd

		info = self._get_authinfo (email)
		if not info:
			return False	# no matched user

		if not info.get ("confirmed"):
			return False	# not confirmed by email

		if info.get ("pwdhash") != self._get_pwdhash (old_pwd, info.get ("pwdtype")):
			return False	# invalid pwd

		info["pwdhash"] = self._get_pwdhash (new_pwd, self.pwdtype)
		info["pwdtype"] = self.pwdtype
		return self._set_authinfo (email, info)

	def issue_confirm_code (self, email):
		info = self._get_authinfo (email)
		if not info:
			return None		# no matched user

		if info.get ("confirmed"):
			return None		# already confirmed by email

		confirmcode = self._new_confirmcode ()
		info["confirmcode"] = confirmcode
		self._set_authinfo (email, info)
		return confirmcode

	def auth_confirm_email (self, email, confirmcode):
		if len (confirmcode) == 0:
			return False

		info = self._get_authinfo (email)
		if not info:
			return False	# no matched user

		if info.get ("confirmcode") != confirmcode:
			return False	# no matched confirmcode

		info["confirmed"] = True
		info["confirmcode"] = None
		self._set_authinfo (email, info)
		return True

	def verify_session (self, email, sessionid):
		sessioninfo = self._get_session (email, sessionid)
		if not sessioninfo:
			return None

		return sessioninfo.get ("expire")

	def _get_pwdhash (self, raw_pwd, pwdtype = None):
		if pwdtype == None:
			pwdtype = "raw"

		if pwdtype == "raw":
			return raw_pwd

		h = hashlib.new (pwdtype)
		h.update (raw_pwd)
		return h.hexdigest ()

	def _get_authinfo (self, email):
		return self.auth_store.get_json (email + self.auth_postfix)

	def _set_authinfo (self, email, authinfo):
		return self.auth_store.set_json (email + self.auth_postfix, authinfo)

	def _new_confirmcode (self):
		return str (uuid.uuid4 ())
		
	def _new_sessionid (self):
		return str (uuid.uuid4 ())

	def _get_session (self, email, sessionid):
		j = self.temp_store.get_json (email + "_" + sessionid)
		if not j:
			return None

		
		if timehelper.deserializeDictToDateTime (j.get ("expire")) < datetime.utcnow ():
			self._del_session (email, sessionid)
			return None

		return j

	def _set_session (self, email, sessionid, sessioninfo):
		return self.temp_store.set_json (email + "_" + sessionid, sessioninfo)

	def _del_session (self, email, sessionid):
		return self.temp_store.dele (email + "_" + sessionid)
