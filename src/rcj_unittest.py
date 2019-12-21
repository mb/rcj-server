#!/usr/bin/env python3

from rcj import Rcj
import unittest
import os

class Test(unittest.TestCase):
	"""Unit test framework for Rcj lib"""
	def test_referee(self):
		self.assertFalse(self.rcj.is_referee('test_user'))
		self.assertFalse(self.rcj.is_referee('test_referee'))
		self.rcj.update_referee('test_user', 'test_pass')
		self.assertTrue(self.rcj.is_referee('test_user'))
		self.assertTrue(self.rcj.check_referee_password('test_user', 'test_pass'))
		self.assertFalse(self.rcj.check_referee_password('test_user', 'other_pass'))
		self.assertFalse(self.rcj.is_referee('test_referee'))

	@classmethod
	def setUpClass(cls):
		cls.rcj = Rcj('unittest.db')
		cls.rcj.create_database('rcj-db.schema')

	@classmethod
	def tearDownClass(cls):
		os.remove('unittest.db')

if __name__ == '__main__':
	unittest.main()
