|logo| Voltaire Quickstart
===========================================

.. |logo|  image:: ../logo.png
           :alt: Voltaire Logo

Voltaire is static site toolkit built on top of Pelican and various other libraries to provide an opinionated, "batteries-included" setup so that you can focus immediately on the actual writing.

You might think of it as an alternative to Pelican's built-in ``quickstart`` where you can inherit improvements automatically on each update.

Quick Start
-----------

Install ``voltaire``:

.. code-block:: bash

   $ pip install voltaire

Voltaire provides build tasks via ``invoke``, so create a ``tasks.py`` containing:

.. code-block:: python

   import voltaire

   namespace = voltaire.site()

You can now see tasks available via ``invoke -l``. As this is now your own ``tasks.py`` file for ``invoke``, you are welcome to add any custom tasks later.

Now we can create a minimal ``pelicanconf.py`` file with just the line:

.. code-block:: python

   from voltaire.pelican import *

Again, this is a normal configuration file for pelican so you can add custom configuration e.g.:

.. code-block:: python

   from voltaire.pelican import *

   SITENAME = "My Website"

Now do ``mkdir content`` and add a single page at ``content/page.md``:

.. code-block:: markdown

   title: My Page

   This is my page.

Now you can run ``invoke build`` to build and you should see an output file at ``output/page/index.html``.

This has built a static site with opinionated defaults.

Features
--------

See all included features.

.. toctree::
   features
