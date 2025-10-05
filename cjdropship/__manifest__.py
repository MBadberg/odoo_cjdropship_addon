# -*- coding: utf-8 -*-
{
    'name': 'CJDropshipping Integration',
    'version': '19.1.0.0.0',
    'category': 'Sales/Sales',
    'summary': 'Integration with CJDropshipping API for product import and order fulfillment',
    'description': """
CJDropshipping Integration for Odoo
====================================

This module provides complete integration with CJDropshipping API:

Compatibility:
--------------
* Odoo 19.0 Community Edition
* Odoo 19.1 Community Edition (including alpha versions)
* No Enterprise Edition features required

Features:
---------
* Import dropshipping products from CJDropshipping catalog
* Automatic order fulfillment
* Real-time inventory and logistics queries
* Webhook integration for order status updates
* Product sync with CJDropshipping
* Automatic price and stock updates

Requirements:
-------------
* CJDropshipping API credentials
* Active CJDropshipping account

Configuration:
--------------
1. Go to Sales > Configuration > CJDropshipping > Settings
2. Enter your API credentials
3. Configure sync settings
4. Import products or enable automatic order fulfillment
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale_management',
        'stock',
        'product',
    ],
    'data': [
        'security/cjdropship_security.xml',
        'security/ir.model.access.csv',
        'data/cjdropship_data.xml',
        'views/cjdropship_config_views.xml',
        'views/cjdropship_product_views.xml',
        'views/cjdropship_order_views.xml',
        'views/cjdropship_webhook_views.xml',
        'views/cjdropship_menus.xml',
        'wizards/product_import_wizard_views.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['requests'],
    },
}
