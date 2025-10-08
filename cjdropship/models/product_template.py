# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_cjdropship = fields.Boolean(string='Is CJDropshipping Product', default=False)
    cjdropship_product_id = fields.Many2one('cjdropship.product',
        string='CJ Product', ondelete='set null', readonly=True)
    cj_product_id = fields.Char(related='cjdropship_product_id.cj_product_id',
        string='CJ Product ID', readonly=True)
    cj_stock_qty = fields.Integer(related='cjdropship_product_id.cj_stock_qty',
        string='CJ Stock', readonly=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_cjdropship = fields.Boolean(related='product_tmpl_id.is_cjdropship',
        string='Is CJDropshipping Product', store=True)
