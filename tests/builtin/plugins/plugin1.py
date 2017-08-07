#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: plugin1
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Provide a brief description of the module.
"""

from ploogz import Ploogin


class TestPlooginOne(Ploogin):

    def __init__(self):
        super().__init__(name='Test Ploogin One')
        self.upon_setup_called = False
        self.upon_activation_called = False
        self.upon_teardown_called = False

    def upon_setup(self):
        self.upon_setup_called = True

    def upon_activation(self):
        self.upon_activation_called = True

    def upon_teardown(self):
        self.upon_teardown_called = True

