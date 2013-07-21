#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kvstorelocal import KVStoreLocal

class KVStore (object):
	LOCAL_STORE = 0

	@classmethod
	def new (cls, type = None, location = "", reset = False):
		if type is None:
			type = KVStore.LOCAL_STORE

		if type == KVStore.LOCAL_STORE:
			kv = KVStoreLocal (path = location)
			if reset:
				kv.dele_all ()
		else:
			raise Exception ("Not supported yet : " + str (type))

		return kv
