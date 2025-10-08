# -*- coding: utf-8 -*-
"""Product Template and Product extensions for CJDropshipping."""

from odoo import models, fields


class ProductTemplate(models.Model):
    """Extension of product.template for CJDropshipping integration."""

    _inherit = 'product.template'

    is_cjdropship = fields.Boolean(
        'Is CJDropshipping Product',
        default=False
    )
    cjdropship_product_id = fields.Many2one(
        'cjdropship.product',
        'CJ Product',
        ondelete='set null',
        readonly=True
    )
    cj_product_id = fields.Char(
        related='cjdropship_product_id.cj_product_id',
        string='CJ Product ID',
        readonly=True
    )
    cj_stock_qty = fields.Integer(
        related='cjdropship_product_id.cj_stock_qty',
        string='CJ Stock',
        readonly=True
    )


class ProductProduct(models.Model):
    """Extension of product.product for CJDropshipping integration."""

    _inherit = 'product.product'

    is_cjdropship = fields.Boolean(
        related='product_tmpl_id.is_cjdropship',
        string='Is CJDropshipping Product',
        store=True
    )
