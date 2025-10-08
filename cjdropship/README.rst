============================
CJDropshipping Integration
============================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

|badge1| |badge2|

This module provides complete integration with CJDropshipping API for Odoo.

**Table of contents**

.. contents::
   :local:

Features
========

* Import dropshipping products from CJDropshipping catalog
* Automatic order fulfillment
* Real-time inventory and logistics queries
* Webhook integration for order status updates
* Product sync with CJDropshipping
* Automatic price and stock updates

Compatibility
=============

* Odoo 19.0 Community Edition
* No Enterprise Edition features required

Requirements
============

* CJDropshipping API credentials
* Active CJDropshipping account
* Python package: requests

Configuration
=============

1. Go to Sales > Configuration > CJDropshipping > Settings
2. Enter your API credentials
3. Click "Test Connection" to verify the connection
4. Configure sync settings and price markup
5. Import products or enable automatic order fulfillment

Usage
=====

Product Import
--------------

* Navigate to CJDropshipping > Configuration > Settings
* Click "Import Products" button
* Or go to CJDropshipping > Products > CJ Products to manage manually

Order Management
----------------

* Automatic: Enable "Auto Fulfill Orders" in settings
* Manual: Open a sales order and click "Send to CJDropshipping"

Webhooks
--------

* Configure the webhook URL in your CJDropshipping dashboard
* Webhooks automatically update order status and tracking information

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/MBadberg/odoo_cjdropship_addon/issues>`_.
In case of trouble, please check there if your issue has already been reported.

Credits
=======

Authors
~~~~~~~

* Markus Badberg IT Spezialist

Contributors
~~~~~~~~~~~~

* Markus Badberg <https://badberg.online>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `MBadberg/odoo_cjdropship_addon
<https://github.com/MBadberg/odoo_cjdropship_addon>`_ project on GitHub.

You are welcome to contribute.
