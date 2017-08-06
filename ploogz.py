#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: ploogz
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Provide a brief description of the module.
"""

import os
import importlib.util
import re
import inspect
from abc import ABCMeta, abstractmethod
from typing import Iterator, List
from automat import MethodicalMachine

__version__ = '0.0.1'  # The working version.
__release__ = '0.0.1'  # The release version.

_DEFAULT_SEARCH_PATH = [
    os.path.normpath(os.path.join(os.getcwd(), 'builtin/plugins'))
]  # The default paths we'll search for plugins.


class Ploogin(object):
    """
    Extend this class to create your own plugins!
    """
    __metaclass__ = ABCMeta

    def __init__(self, name: str):
        """

        :param name: a helpful, descriptive, human-readable name for the plugin
        :type name:  ``str``
        """
        super().__init__()
        self._name = name

    @property
    def name(self) -> str:
        """
        Get the helpful, descriptive, human-readable name for the plugin

        :rtype: ``str``
        """
        return self._name

    @abstractmethod
    def setup(self):
        """
        Override this method to perform setup on the plugin.  After this method is called, your plugin should be ready
        for the ``activate()`` method to be called so it can start doing its thing.

        :seealso: :py:func:`Ploogin.activate`
        """
        pass

    @abstractmethod
    def activate(self):
        """
        Override this method to have the plugin do its principal work.
        """
        pass

    @abstractmethod
    def teardown(self):
        """
        Override this method perform steps required when the application using the plugin decides that its work is
        done.
        """
        pass


class PlooginHost(object):
    """
    Use a host object to load and retrieve your ploogins.
    """
    _path_sep_re = re.compile(r":?[\\/\s]", re.IGNORECASE)  # A regular expression that matches file path separators.
    _machine = MethodicalMachine()  # This is the class state machine.

    def __init__(self, search_path: List[str] or str=None):
        """

        :param search_path: the paths the plugin host will search when the ``load()`` method is called
        :type search_path:  List[str] or ``str``
        :seealso: :py:func:`PlooginHost.load`

        .. note::
            If no search path is provided, the default path is ``builtin/plugins`` under the current working directory.
        """
        # Lets figure out what we got for the search path as a parameter value, and turn it into something we can use
        # as we activate along.  (The code below seemed like the more readable wat
        _search_path = None
        if isinstance(search_path, list):
            _search_path = search_path
        elif isinstance(search_path, str):
            _search_path = [search_path]
        elif _search_path is None:
            _search_path = _DEFAULT_SEARCH_PATH
        else:
            raise TypeError('The search_path parameters must be a string or list of strings.')
        # What we want in a search path is a list of paths normalized for the operating system.  So, we'll start
        # either with the prescribed list of search paths, and apply the path.normpath() function to each one.
        self._search_path = list(map(lambda p: os.path.normpath(p),  _search_path))
        # Create a variable for the plugins, but don't populate it with a value yet.  (We'll do that when somebody
        # calls the load() function.)
        self._plugins = None

    @_machine.state(initial=True)
    def not_loaded(self):
        """The plugins have not been loaded yet."""

    @_machine.state()
    def loaded(self):
        """The plugins have been loaded."""

    @_machine.state()
    def torn_down(self):
        """The plugin host has been torn down."""

    @_machine.input()
    def load(self):
        """
        Load the plugins.
        """

    @_machine.output()
    def _load(self):
        """
        This is the output method associated with the :py:func:`PlooginHost.load` method.

        :seealso: :py:func:`PlooginHost.load`
        """
        # Clear the current list of plugins.
        self._plugins = []
        # We're going to build up a list of files that may contain modules.
        candidate_module_files = []
        # We need to activate through every search path in the list of search paths.
        for path in self._search_path:
            # We're going to walk the directory hierarchy.
            for (dirpath, _, filenames) in os.walk(path):
                # Let's look at each filename...
                for filename in filenames:
                    # ...we're only interested in the python modules.
                    if filename.endswith('.py'):
                        # We have a candidate!  Add this module file to the list.  (We'll look for actual plugins
                        # later.)
                        candidate_module_files.append(os.sep.join([dirpath, filename]))
        # Now let's activate look at those files!
        for candidate_module_file in candidate_module_files:
            # We need to give the module a name.  Let's base it on the file path.
            module_name = PlooginHost._path_to_module_name(os.path.splitext(candidate_module_file)[0])
            # Now let's import the module.
            spec = importlib.util.spec_from_file_location(module_name, candidate_module_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            # For our next trick, we'll need all the module members.
            members = [member for _, member in inspect.getmembers(mod)]
            # But we only want those members that inherit from Ploogin.
            plugin_classes = filter(lambda member: inspect.isclass(member) and Ploogin in member.__bases__, members)
            # Instantiate each plugin class and put the instance in the list.
            for cls in plugin_classes:
                self._plugins.append(cls())

    @_machine.input()
    def teardown(self):
        """
        Call this method when you're finished with this plugin host, and all the plugins it has provided.

        :seealso: :py:func:`Ploogin.teardown`
        """

    @_machine.output()
    def _teardown(self):
        """
        This is the output method associated with the :py:func:`PlooginHost.teardown` method.

        :seealso: :py:func:`PlooginHost.teardown`
        :seealso: :py:func:`Ploogin.teardown`
        """
        # Tear down all the plugins.
        map(lambda plugin: plugin.teardown(), self._plugins)
        # Clear out the list.
        self._plugins = []

    @property
    def plugins(self) -> Iterator[Ploogin]:
        """
        Get the plugins loaded by this host.

        :rtype: :py:class:`Ploogin`
        """
        return iter(self._plugins) if self._plugins is not None else iter([])

    @staticmethod
    def _path_to_module_name(path: str) -> str:
        """
        Convert a file system path to a module path that can be used when dynamically loading modules.

        :param path: a file system path
        :type path:  ``str``
        :return: the path, converted to conform to a python module name
        :rtype:  ``str``
        """
        return PlooginHost._path_sep_re.sub('.', path)

    # We start in the 'not_loaded' state until somebody calls load(), at which point we call the _load() function and
    # move to the 'loaded' state.
    not_loaded.upon(load, enter=loaded, outputs=[_load])
    # If we're in the 'loaded' state and somebody calls 'teardown', call _teardown() and move to the 'torn_down' state.
    loaded.upon(teardown, enter=torn_down, outputs=[_teardown])
