#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, shutil
import kvstorelocal

class KVStoreLocal_Test (unittest.TestCase):
	def setUp (self):
		if os.path.exists ("sandbox"):
			shutil.rmtree ("sandbox")
		os.makedirs ("sandbox/tmp")
		self.store = kvstorelocal.KVStoreLocal (path="sandbox/tmp")

	def test_text (self):
		k = u"this is a key string"
		v = u"this is value text\nlet's goto the school.\nfin."
		self.assertTrue (self.store.set_text (k, v))
		self.assertEqual (self.store.get_text (k), v)

	def test_json (self):
		k = u"this is a key string for json value"
		v = {
			"json" : {
				"users" : [
					{
						"name" : "foo",
						"pass" : "1234",
						"age" : 5,
						"description" : u"foo is a bear."
					},
					{
						"name" : "bar",
						"pass" : "\12\34\56\78",
						"age" : 1,
						"description" : "bar is a honey."
					}
				],
				"departments" : [
					{
						"name" : "animals likes honey",
						"consist of" : [
							"foo",
							"bar"
						]
					}
				]
			}
		}
		self.assertTrue (self.store.set_json (k, v))
		self.assertEqual (self.store.get_json (k), v)

	def test_binary (self):
		k = u"this is a key string for binary value"
		v = ""
		if sys.platform == "win32":
			with open ("/windows/system32/notepad.exe", "rb") as f:
				v = f.read ()
		else:
			with open ("/bin/bash", "rb") as f:
				v = f.read ()
		self.assertTrue (self.store.set_binary (k, v))
		self.assertEqual (self.store.get_binary (k), v)

if __name__ == "__main__":
	unittest.main ()
