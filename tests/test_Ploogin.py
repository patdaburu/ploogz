#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_Ploogin
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Unit tests of the :py:class:`ploogz.Ploogin` class.
"""

import unittest
from automat import NoTransition
from ploogz import Ploogin


class TestPloogin(Ploogin):

    def __init__(self):
        super().__init__(name='Test Ploog')
        self.upon_setup_called = False
        self.upon_activation_called = False
        self.upon_teardown_called = False

    def upon_setup(self):
        self.upon_setup_called = True

    def upon_activation(self):
        self.upon_activation_called = True

    def upon_teardown(self):
        self.upon_teardown_called = True


class TestPlooginSuite(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_inheritPloogin_initialize_verifyProperties(self):
        test_ploogin = TestPloogin()
        self.assertEqual('Test Ploog', test_ploogin.name)

    def test_inheritPloogin_setup_verifyOnSetupCalled(self):
        test_ploogin = TestPloogin()
        test_ploogin.setup()
        self.assertTrue(test_ploogin.upon_setup_called)
        self.assertFalse(test_ploogin.upon_activation_called)
        self.assertFalse(test_ploogin.upon_teardown_called)

    def test_inheritPloogin_setupAndActivate_verifyOnActivationCalled(self):
        test_ploogin = TestPloogin()
        test_ploogin.setup()
        test_ploogin.activate()
        self.assertTrue(test_ploogin.upon_setup_called)
        self.assertTrue(test_ploogin.upon_activation_called)
        self.assertFalse(test_ploogin.upon_teardown_called)

    def test_inheritPloogin_setupActivateTeardown_verifyOnTeardownCalled(self):
        test_ploogin = TestPloogin()
        test_ploogin.setup()
        test_ploogin.activate()
        test_ploogin.teardown()
        self.assertTrue(test_ploogin.upon_setup_called)
        self.assertTrue(test_ploogin.upon_activation_called)
        self.assertTrue(test_ploogin.upon_teardown_called)

    def test_inheritPloogin_activateWithoutSetup_verifyNoTransition(self):
        test_ploogin = TestPloogin()
        with self.assertRaises(NoTransition):
            test_ploogin.activate()

