.. ploogz documentation master file, created by
   sphinx-quickstart on Sun Aug  6 12:37:26 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ploogz:  A simple python plugin framework.
==========================================

Ploog it in and go.

To get the source, visit the `github repository <https://github.com/patdaburu/ploogz>`_.

.. toctree::
    :glob:
    :maxdepth: 2

    api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Quickstart
==========

ploogz is a pretty simple plugin framework, so there isn't a whole lot to know to get started.  Step one is to extend
the :py:class:`ploogz.ploogins.Ploogin` class and override the important methods to create an object that can do some
useful work.  (In the code blocks below, we don't include docstrings to focus on the code itself... *but you should
always document your code!*)

.. code-block:: python

    from ploogz.ploogins import Ploogin


    class MyUsefulThing(Ploogin):

        def __init__(self):
            super().__init__(name='My Useful Thing')

        def upon_setup(self):
            print("Getting ready!")

        def upon_activation(self):
            print("Here we go!!")

        def upon_teardown(self):
            print("Good night.")

You can place this class in a python file (with a ``.py`` extension) in a directory along with other files containing
other ploogins.

When it comes time to load these useful classes into an application, you'll need a
:py:class:`ploogz.ploogins.PlooginHost`.

.. code-block:: python

    from ploogz.ploogins import PlooginHost

    host = PlooginHost(search_path=['/path/to/ploogins/directory', '/another/path/to/more/ploogins'])
    host.load()
    for ploogin in host.ploogins:
        ploogin.setup()
    for ploogin in host.ploogins:
        ploogin.activate()
    # When you're all done, you can call teardown() on the host which will tear down all the ploogins.
    host.teardown()

In the simplest terms, that's all there is to it.  This library is in the early stages of its development and there
will likely be some additions, but these examples demonstrate the simple approach we seek.
