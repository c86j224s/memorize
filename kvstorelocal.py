#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib, json, os, os.path, shutil

class KVStoreLocal (object):
	def __init__ (self, path = u"./"):
		self._path = path

	def __del__ (self):
		pass

	def set_binary (self, key, value):
		try:
			with open (self._get_key (key), "wb") as s:
				s.write (value)
		except:
			return False
		return True

	def set_text (self, key, value):
		try:
			with open (self._get_key (key), "w") as s:
				s.write (value)
		except:
			return False
		return True
	
	def set_json (self, key, value):
		try:
			with open (self._get_key (key), "w") as s:
				s.write (json.dumps (value))
		finally: pass
		#except:
		#	return False
		return True

	def get_binary (self, key):
		v = None
		try:
			with open (self._get_key (key), "rb") as s:
				v = s.read ()
		except:
			pass
		return v
	
	def get_json (self, key):
		v = None
		try:
			with open (self._get_key (key), "r") as s:
				v = json.loads (s.read ())
		except:
			pass
		return v
	
	def get_text (self, key):
		v = None
		try:
			with open (self._get_key (key), "r") as s:
				v = s.read ()
		except:
			pass
		return v

	def dele (self, key):
		os.remove (self._get_key (key))
		return True

	def dele_all (self):
		if os.path.exists (self._path):
			shutil.rmtree (self._path)
		os.makedirs (self._path)
		return True

	def _get_key (self, raw_key):
		h = hashlib.sha256 ()
		h.update (raw_key)
		return self._path + "/" + h.hexdigest ()
