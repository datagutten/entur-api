=============
Entur API
=============

Tools to work with Enturs API

Quick start
-----------

1. Add "entur-monitor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'entur-api',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('entur-monitor/', include('entur-monitor.urls')),

