# -*- coding: utf-8 -*-
"""CJDropshipping Product Model."""

import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CJDropshippingProduct(models.Model):
    """Model for storing CJDropshipping product information."""

    _name = 'cjdropship.product'
    _description = 'CJDropshipping Product'
    _rec_name = 'cj_product_name'

    # CJDropshipping Fields
    cj_product_id = fields.Char(
        'CJ Product ID',
        required=True,
        index=True
    )
    cj_product_name = fields.Char('CJ Product Name', required=True)
    cj_product_sku = fields.Char('CJ SKU')
    cj_variant_id = fields.Char('CJ Variant ID', index=True)

    # Product Information
    description = fields.Text()
    category_name = fields.Char('CJ Category')

    # Pricing
    cj_price = fields.Float('CJ Price', digits='Product Price')
    selling_price = fields.Float(digits='Product Price')

    # Inventory
    cj_stock_qty = fields.Integer('CJ Stock Quantity')

    # Images
    image_url = fields.Char('Image URL')
    image_urls = fields.Text('Additional Images (JSON)')

    # Shipping
    shipping_weight = fields.Float('Shipping Weight (kg)')
    shipping_length = fields.Float('Length (cm)')
    shipping_width = fields.Float('Width (cm)')
    shipping_height = fields.Float('Height (cm)')

    # Relations
    product_tmpl_id = fields.Many2one(
        'product.template',
        'Odoo Product',
        ondelete='set null',
        index=True
    )
    config_id = fields.Many2one(
        'cjdropship.config',
        'Configuration',
        required=True,
        default=lambda self: (
            self.env['cjdropship.config'].get_default_config()
        )
    )

    # Status
    active = fields.Boolean(default=True)
    sync_date = fields.Datetime('Last Sync Date')

    _sql_constraints = [
        (
            'cj_product_variant_unique',
            'unique(cj_product_id, cj_variant_id)',
            'CJ Product and Variant combination must be unique!'
        )
    ]

    def action_create_odoo_product(self):
        """Create or update Odoo product from CJ product."""
        self.ensure_one()

        product_template_model = self.env['product.template']

        # Prepare product values
        categ_id = False
        if self.config_id.default_categ_id:
            categ_id = self.config_id.default_categ_id.id
        vals = {
            'name': self.cj_product_name,
            'type': self.config_id.default_product_type,
            'categ_id': categ_id,
            'list_price': self.selling_price,
            'standard_price': self.cj_price,
            'description_sale': self.description,
            'weight': self.shipping_weight,
            'cjdropship_product_id': self.id,
            'is_cjdropship': True,
        }

        if self.cj_product_sku:
            vals['default_code'] = self.cj_product_sku

        if self.product_tmpl_id:
            # Update existing product
            self.product_tmpl_id.write(vals)
            product = self.product_tmpl_id
        else:
            # Create new product
            product = product_template_model.create(vals)
            self.product_tmpl_id = product.id

        # Download and set image if URL is available
        if self.image_url:
            try:
                import base64
                import requests
                response = requests.get(self.image_url, timeout=10)
                if response.status_code == 200:
                    product.image_1920 = base64.b64encode(response.content)
            except Exception as exc:
                _logger.warning(
                    "Failed to download product image: %s", str(exc)
                )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'res_id': product.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_sync_from_cj(self):
        """Sync product data from CJDropshipping."""
        self.ensure_one()

        try:
            client = self.config_id.get_api_client()

            # Get product details
            product_data = client.get_product_detail(self.cj_product_id)

            if not product_data:
                raise UserError(
                    self.env._('Product not found in CJDropshipping')
                )

            # Update fields
            update_vals = {
                'cj_product_name': product_data.get(
                    'productNameEn',
                    self.cj_product_name
                ),
                'description': product_data.get('description', ''),
                'cj_price': float(product_data.get('sellPrice', 0)),
                'sync_date': fields.Datetime.now(),
            }

            # Recalculate selling price
            update_vals['selling_price'] = (
                self.config_id.calculate_sale_price(update_vals['cj_price'])
            )

            # Get inventory
            try:
                inventory_data = client.get_product_inventory(
                    self.cj_product_id,
                    self.cj_variant_id
                )
                if inventory_data:
                    update_vals['cj_stock_qty'] = int(
                        inventory_data.get('quantity', 0)
                    )
            except Exception as exc:
                _logger.warning(
                    "Failed to get inventory for %s: %s",
                    self.cj_product_id,
                    str(exc)
                )

            self.write(update_vals)

            # Update linked Odoo product if exists
            if self.product_tmpl_id:
                self.product_tmpl_id.write({
                    'list_price': update_vals['selling_price'],
                    'standard_price': update_vals['cj_price'],
                })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': self.env._('Success'),
                    'message': self.env._('Product synced successfully'),
                    'type': 'success',
                }
            }
        except Exception as exc:
            _logger.error(
                "Failed to sync product %s: %s",
                self.cj_product_id,
                str(exc)
            )
            raise UserError(
                self.env._('Failed to sync product: %s', str(exc))
            ) from exc

    def action_bulk_create_products(self):
        """Create Odoo products for multiple CJ products."""
        for record in self:
            if not record.product_tmpl_id:
                record.action_create_odoo_product()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': self.env._('Success'),
                'message': self.env._(
                    '%d products created successfully',
                    len(self)
                ),
                'type': 'success',
            }
        }
