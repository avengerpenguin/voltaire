Features
========

Plantuml
--------

Voltaire has ``plantuml_markdown`` enabled by default so any markdown file with ``plantuml`` code blocks will have them automatically replaced by SVGs.

Google Analytics 4
------------------

Add the ``G-`` measurement ID from your Google Analytics 4 web data stream to
``publishconf.py`` so analytics is only included in published builds:

.. code-block:: python

   GA4_MEASUREMENT_ID = "G-XXXXXXXXXX"

Voltaire loads the Google tag and configures the supplied GA4 measurement ID.
The older setting name ``GOOGLE_TAG_ID`` remains supported as a compatibility
alias, but new sites should use ``GA4_MEASUREMENT_ID``. A ``G-`` measurement ID
is not a Google Tag Manager container ID; Tag Manager IDs start with ``GTM-``.

Universal Analytics ``UA-`` properties and the old ``GOOGLE_ANALYTICS_ID``
setting are not supported because Universal Analytics no longer processes
data.

Outbound and affiliate links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GA4 Enhanced Measurement can record ordinary outbound links as the standard
``click`` event. Enable outbound click measurement in the web data stream; do
not mark that broad event as a key event unless every outbound link should be
counted as a conversion.

Voltaire emits a separate ``affiliate_click`` event when a link has
``rel="sponsored"`` or matches an ``AFFILIATE_RULES`` entry. For example:

.. code-block:: html

   <a href="https://merchant.example/product" rel="sponsored">Buy it</a>

Rules can identify existing affiliate URLs by domain and, where needed, require
a query parameter:

.. code-block:: python

   AFFILIATE_RULES = [
       {
           "domain": "amazon.co.uk",
           "query_parameter": "tag",
           "network": "amazon",
       },
       {"domain": "awin1.com", "network": "awin"},
   ]

Domain rules match the named domain and its subdomains. ``query_parameter`` and
``network`` are optional. A sponsored link can provide a network without a rule
using ``data-affiliate-network="amazon"``.

The event contains ``link_url``, ``link_domain`` and ``link_text``, plus
``affiliate_network`` when known. Mark ``affiliate_click`` as a key event in
each applicable GA4 property, then test it with Realtime or DebugView.

Consent
~~~~~~~

Voltaire does not supply a consent banner or consent management platform. Site
owners are responsible for integrating an appropriate CMP where consent is
required. A Consent Mode default alone is not a consent interface.

When a certified CMP implements the IAB Transparency and Consent Framework,
enable Voltaire's TCF-aware Google Consent Mode integration in
``publishconf.py``:

.. code-block:: python

   GOOGLE_TCF_CONSENT_MODE = True

This enables Google's TCF support and, before any Google tag loads, sets Consent
Mode v2 defaults to ``denied`` for the EEA, UK and Switzerland. The CMP must
then collect the visitor's choice and expose a valid TCF consent signal. Do not
enable this setting as a substitute for installing and publishing the CMP.

Sites serving AdSense ads to visitors in those regions must use a
Google-certified CMP integrated with TCF. This can be Google's Privacy &
messaging CMP configured in AdSense or another certified CMP. Confirm that the
message is published for every relevant domain and that consent choices reach
both AdSense and GA4. Validate the default and update signals with Tag Assistant
and verify the CMP's ``__tcfapi`` in a browser.


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
