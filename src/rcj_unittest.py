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
            'scoring': {
                'teamStarted': True,
                'evacuationPoint': "high",
                'sections': [],
                'victims': {
                    'deadVictimsBeforeAllLivingVictims': 3,
                    'livingVictims': 2,
                    'deadVictimsAfterAllLivingVictims': 0
                },
                'leftEvacuationZone': False,
                'score': 314
            },
            'score': 314,
            'comments': 'comments from referees',
            'complaints': '',
            'confirmed': True,
        }
        self.rcj.store_run(run)

    def test_score_example_dss(self):
        scoring = {
            'teamStarted': True,
            'evacuationPoint': 'low',
            'sections': [{
                'sectionId': 1,
                'completedSection': False,
                'skippedSection': False,
                'lops': 0,
                'isAfterLastCheckpoint': False,
                'gaps': 0,
                'obstacles': 0,
                'speedbumps': 0,
                'ramps': 0,
                'intersections': 0,
                'tiles': 0
            }],
            'victims': {
                'deadVictimsBeforeAllLivingVictims': 0,
                'livingVictims': 0,
                'deadVictimsAfterAllLivingVictims': 0
            },
            'leftEvacuationZone': False,
            'score': 5
        }
        score = 5
        self.assertEqual(score, self.rcj.calculate_score(scoring))

    @classmethod
    def setUpClass(cls):
        if os.path.isfile('unittest.db'):
            os.remove('unittest.db')
        cls.rcj = Rcj('unittest.db')
        cls.rcj.init_database('rcj_db.schema')

    @classmethod
    def tearDownClass(cls):
        os.remove('unittest.db')

if __name__ == '__main__':
    unittest.main()
