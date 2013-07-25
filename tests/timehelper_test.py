#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, datetime, json
import timehelper

class TimeHelper_Test (unittest.TestCase):
	def setUp (self):
		pass
		
	def test_serialize_deserialize (self):
		dt = datetime.datetime.utcnow ()
		
		d = timehelper.serializeDateTimeToDict (dt)
		self.assertNotEqual (d, None)
		
		j = json.dumps (d)
		
		d2 = json.loads (j)
		
		self.assertEqual (d, d2)
		
		dt2 = timehelper.deserializeDictToDateTime (d2)
		self.assertNotEqual (dt2, None)
		
		self.assertEqual (dt, dt2)
	
	#
	# this does not work in python 2.x
	#
	#def test_add_sub (self):
	#	dt = datetime.datetime.utcnow ()
	#	
	#	assertTrue (dt + 100, dt + datetime.timedelta (second=100))
	#	
	#	assertTrue (dt - 100, dt - datetime.timedelta (second=100))
	#