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
    
    def test_run(self):
        self.rcj.update_referee('referee_run', 'some_pw')
        scoring = '''{
            teamStarted: true,
            evacuationPoint: "high",
            sections: [ ... ],
            victims: {
                deadVictimsBeforeAllLivingVictims: 3,
                livingVictims: 2,
                deadVictimsAfterAllLivingVictims: 0
            },
            leftEvacuationZone: false,
            score: 314
        }'''.replace(' ', '').replace('\t', '').replace('\n', '')
        self.rcj.store_run(
            'line',
            'pi++',
            1,
            'A',
            'referee_run',
            120.01,
            1576934336,
            1576934456,
            scoring,
            'comments from referees',
            'comlaining',
            True
        )

    @classmethod
    def setUpClass(cls):
        if os.path.isfile('unittest.db'):
            os.remove('unittest.db')
        cls.rcj = Rcj('unittest.db')
        cls.rcj.create_database('rcj_db.schema')

    @classmethod
    def tearDownClass(cls):
        os.remove('unittest.db')

if __name__ == '__main__':
    unittest.main()
