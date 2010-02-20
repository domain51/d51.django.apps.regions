d51.django.apps.regions
=======================
Django app for connecting models to regions, regardless of types


Introduction
------------
You often need to attach models in Django to some sort of geographic
information.  ``d51.django.apps.regions`` provides a simple, reusable Django
app for attaching a region to a model.

The ``regions`` app provides the ``Region`` model.  ``Region`` serves as the
entry-point to the app.  It is a hierarchical model, and can be related to most
types of geometry within `GeoDjango <http://geodjango.com>`_.

.. TODO: Should be updated once all types are supported


Installation
------------
Create a clone of the repository:

::

    git clone git://github.com/domain51/d51.django.apps.region.git

Then, inside that directory you can install it using either the `setup.py` file
directly, or via Fabric:

::

    prompt> python setup.py install
    ... or ...
    prompt> fab install


Usage
-----
*TODO*


