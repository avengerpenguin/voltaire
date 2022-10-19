Features
========

Plantuml
--------

Voltaire has ``plantuml_markdown`` enabled by default so any markdown file with ``plantuml`` code blocks will have them automatically replaced by SVGs.

Google Analytics
----------------

To add Google Analytics to your site, go through the usual steps in the Google Analytics interface and when you are given a snippet like:

.. code-block:: javascript

    <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    ga('create', '<YOUR_GOOGLE_ANALYTICS_ID>', 'auto');
    ga('send', 'pageview');
    </script>

Get the ID they give for ``<YOUR_GOOGLE_ANALYTICS_ID>`` above and add it to your ``publishconf.py`` (so it's only added in published builds) like this:

.. code-block:: python

   GOOGLE_ANALYTICS_ID = "YOUR ID"


Google Tag Manager
------------------

Similar to above, if you get a snippet from Google like:

.. code-block:: javascript

    <script async src="https://www.googletagmanager.com/gtag/js?id=GOOGLE_TAG_ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'GOOGLE_TAG_ID');
    </script>

You can add this to ``publishconfig.py`` as:

.. code-block:: python

   GOOGLE_TAG_ID = "My tag ID"


Custom CSS Styles
-----------------

Voltaire out of the box uses `awsm.css <https://igoradamenko.github.io/awsm.css/>`_ to provide a sensible baseline plus some extra defaults added by Voltaire itself.

If you wish to custom your styles, create a file at the path ``static/css/style.scss`` and write any valid SCSS in that file.

Note that Voltaire currently only looks for a single file with that exact path.


Disqus Comments
---------------

If you wish to add comments to your pages and posts, Voltaire supports adding Disqus automatically to the bottom of each page and article.

To use this, add the Disque site name ID to your ``publishconf.py`` e.g.:

.. code-block:: python

   DISQUS_SITE = "mysiteid"
