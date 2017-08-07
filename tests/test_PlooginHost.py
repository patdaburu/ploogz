#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_PlooginHost
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Unit tests of the :py:class:`ploogz.PlooginHost` class.
"""

import os
import unittest
from ploogz.ploogins import PlooginHost, Ploogin


class TestFsPlooginLoaderSuite(unittest.TestCase):

    default_search_path = [
        os.path.normpath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'builtin/plugins')
        )
    ]  # The path to the test ploogins.

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_createHostWithDefaultLoader_load_verifyLoaded(self):
        host = PlooginHost(search_path=self.default_search_path)
        host.load()
        ploogins = list(host.ploogins)
        self.assertEqual(2, len(ploogins))
        expected_ploogin_names = ['Test Ploogin One', 'Test Ploogin Two']
        for ploogin in ploogins:
            # Make sure each object we loaded is a Ploogin.
            self.assertTrue(isinstance(ploogin, Ploogin))
            # Make sure we got the expected names.
            self.assertTrue(ploogin.name in expected_ploogin_names)
            # Remove this ploogin's name.  (We don't expect to see it again.)
            expected_ploogin_names = list(filter(lambda name: name != ploogin.name, expected_ploogin_names))
        host.teardown()