#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: plugin2
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Provide a brief description of the module.
"""

from ploogz.ploogins import Ploogin


class TestPlooginTwo(Ploogin):

    def __init__(self):
        super().__init__(name='Test Ploogin Two')
        self.upon_setup_called = False
        self.upon_activation_called = False
        self.upon_teardown_called = False
        self.options = None

    def upon_setup(self, options: dict=None):
        self.options = options
        self.upon_setup_called = True

    def upon_activation(self):
        self.upon_activation_called = True

    def upon_teardown(self):
        self.upon_teardown_called = True

