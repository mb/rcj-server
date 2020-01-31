#!/usr/bin/env python3

from rcj import Rcj
import unittest
import os
import json

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
        run = {
            'competition': 'line',
            'teamname': 'pi++',
            'round': 3,
            'arena': 'A',
            'referee': 'referee_run',
            'time_duration': 120,
            'time_start': 1576934336,
            'time_end': 1576934456,
            'scoring': '''{
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
            }'''.replace(' ', '').replace('\t', '').replace('\n', ''),
            'score': 314,
            'comments': 'comments from referees',
            'complaints': '',
            'confirmed': True,
        }
        self.rcj.store_run(run)

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
