# -*- coding: utf-8 -*-
"""CJDropshipping Product Import Wizard."""

import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductImportWizard(models.TransientModel):
    """Wizard for importing products from CJDropshipping."""

    _name = 'cjdropship.product.import.wizard'
    _description = 'CJDropshipping Product Import Wizard'

    config_id = fields.Many2one(
        'cjdropship.config',
        'Configuration',
        required=True,
        default=lambda self: (
            self.env['cjdropship.config'].get_default_config()
        )
    )

    category_id = fields.Many2one(
        'product.category',
        'Category Filter',
        help='Filter products by CJDropshipping category'
    )

    page_number = fields.Integer(
        default=1,
        required=True
    )
    page_size = fields.Integer(
        'Products per Page',
        default=20,
        required=True
    )

    create_odoo_products = fields.Boolean(
        'Create Odoo Products Immediately',
        default=False,
        help='Automatically create Odoo products after import'
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('importing', 'Importing'),
            ('done', 'Done'),
        ],
        default='draft'
    )

    imported_count = fields.Integer(readonly=True)
    error_message = fields.Text(readonly=True)

    def action_import_products(self):
        """Import products from CJDropshipping."""
        self.ensure_one()

        try:
            self.state = 'importing'

            client = self.config_id.get_api_client()

            # Get product list
            result = client.get_product_list(
                page=self.page_number,
                page_size=self.page_size,
                category_id=self.category_id.id if self.category_id else None
            )

            if not result or not result.get('list'):
                raise UserError(self.env._('No products found'))

            products_data = result.get('list', [])
            imported_count = 0

            cj_product_model = self.env['cjdropship.product']

            for product_data in products_data:
                try:
                    product_id = product_data.get('pid')
                    if not product_id:
                        continue

                    # Check if product already exists
                    existing = cj_product_model.search([
                        ('cj_product_id', '=', product_id),
                        ('cj_variant_id', '=', False)
                    ], limit=1)

                    # Prepare product values
                    vals = {
                        'cj_product_id': product_id,
                        'cj_product_name': product_data.get('productNameEn', ''),
                        'cj_product_sku': product_data.get('productSku', ''),
                        'description': product_data.get('description', ''),
                        'cj_price': float(product_data.get('sellPrice', 0)),
                        'category_name': product_data.get('categoryName', ''),
                        'image_url': product_data.get('productImage', ''),
                        'shipping_weight': float(product_data.get('weight', 0)),
                        'config_id': self.config_id.id,
                        'sync_date': fields.Datetime.now(),
                    }

                    # Calculate selling price
                    vals['selling_price'] = (
                        self.config_id.calculate_sale_price(vals['cj_price'])
                    )

                    if existing:
                        existing.write(vals)
                        cj_product = existing
                    else:
                        cj_product = cj_product_model.create(vals)

                    # Create Odoo product if requested
                    if (
                        self.create_odoo_products
                        and not cj_product.product_tmpl_id
                    ):
                        cj_product.action_create_odoo_product()

                    imported_count += 1

                except Exception as exc:
                    _logger.warning(
                        "Failed to import product %s: %s",
                        product_data.get('pid'),
                        str(exc)
                    )
                    continue

            self.write({
                'state': 'done',
                'imported_count': imported_count,
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': self.env._('Success'),
                    'message': self.env._(
                        '%d products imported successfully',
                        imported_count
                    ),
                    'type': 'success',
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }

        except Exception as exc:
            error_msg = str(exc)
            _logger.error("Product import failed: %s", error_msg)

            self.write({
                'state': 'draft',
                'error_message': error_msg,
            })

            raise UserError(
                self.env._('Import failed: %s', error_msg)
            ) from exc

    def action_view_imported_products(self):
        """View imported products."""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Imported CJDropshipping Products'),
            'res_model': 'cjdropship.product',
            'view_mode': 'tree,form',
            'domain': [('config_id', '=', self.config_id.id)],
            'context': {'create': False},
        }
