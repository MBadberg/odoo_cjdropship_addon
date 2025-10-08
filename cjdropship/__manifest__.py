{
    'name': 'CJDropshipping Integration',
    'version': '19.1.0.0.0',
    'category': 'Sales/Sales',
    'summary': (
        'Integration with CJDropshipping API for product import '
        'and order fulfillment'
    ),
    'author': 'Markus Badberg IT Spezialist, Odoo Community Association (OCA)',
    'website': 'https://badberg.online',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'sale_management',
        'stock',
        'product',
    ],
    'data': [
        'security/cjdropship_security.xml',
        'security/ir.model.access.csv',
        'data/cjdropship_data.xml',
        'views/cjdropship_product_views.xml',
        'views/cjdropship_order_views.xml',
        'views/cjdropship_webhook_views.xml',
        'views/cjdropship_config_views.xml',
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
