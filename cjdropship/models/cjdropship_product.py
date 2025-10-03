# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CJDropshippingProduct(models.Model):
    _name = 'cjdropship.product'
    _description = 'CJDropshipping Product'
    _rec_name = 'cj_product_name'
    
    # CJDropshipping Fields
    cj_product_id = fields.Char(string='CJ Product ID', required=True, index=True)
    cj_product_name = fields.Char(string='CJ Product Name', required=True)
    cj_product_sku = fields.Char(string='CJ SKU')
    cj_variant_id = fields.Char(string='CJ Variant ID', index=True)
    
    # Product Information
    description = fields.Text(string='Description')
    category_name = fields.Char(string='CJ Category')
    
    # Pricing
    cj_price = fields.Float(string='CJ Price', digits='Product Price')
    selling_price = fields.Float(string='Selling Price', digits='Product Price')
    
    # Inventory
    cj_stock_qty = fields.Integer(string='CJ Stock Quantity')
    
    # Images
    image_url = fields.Char(string='Image URL')
    image_urls = fields.Text(string='Additional Images (JSON)')
    
    # Shipping
    shipping_weight = fields.Float(string='Shipping Weight (kg)')
    shipping_length = fields.Float(string='Length (cm)')
    shipping_width = fields.Float(string='Width (cm)')
    shipping_height = fields.Float(string='Height (cm)')
    
    # Relations
    product_tmpl_id = fields.Many2one('product.template', string='Odoo Product',
        ondelete='set null', index=True)
    config_id = fields.Many2one('cjdropship.config', string='Configuration',
        required=True, default=lambda self: self.env['cjdropship.config'].get_default_config())
    
    # Status
    active = fields.Boolean(string='Active', default=True)
    sync_date = fields.Datetime(string='Last Sync Date')
    
    _sql_constraints = [
        ('cj_product_variant_unique', 'unique(cj_product_id, cj_variant_id)',
         'CJ Product and Variant combination must be unique!')
    ]
    
    def action_create_odoo_product(self):
        """Create or update Odoo product from CJ product"""
        self.ensure_one()
        
        ProductTemplate = self.env['product.template']
        
        # Prepare product values
        vals = {
            'name': self.cj_product_name,
            'type': self.config_id.default_product_type,
            'categ_id': self.config_id.default_categ_id.id if self.config_id.default_categ_id else False,
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
            product = ProductTemplate.create(vals)
            self.product_tmpl_id = product.id
        
        # Download and set image if URL is available
        if self.image_url:
            try:
                import requests
                response = requests.get(self.image_url, timeout=10)
                if response.status_code == 200:
                    import base64
                    product.image_1920 = base64.b64encode(response.content)
            except Exception as e:
                _logger.warning(f"Failed to download product image: {str(e)}")
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'res_id': product.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_sync_from_cj(self):
        """Sync product data from CJDropshipping"""
        self.ensure_one()
        
        try:
            api = self.config_id.get_api_client()
            
            # Get product details
            product_data = api.get_product_detail(self.cj_product_id)
            
            if not product_data:
                raise UserError(_('Product not found in CJDropshipping'))
            
            # Update fields
            update_vals = {
                'cj_product_name': product_data.get('productNameEn', self.cj_product_name),
                'description': product_data.get('description', ''),
                'cj_price': float(product_data.get('sellPrice', 0)),
                'sync_date': fields.Datetime.now(),
            }
            
            # Recalculate selling price
            update_vals['selling_price'] = self.config_id.calculate_sale_price(update_vals['cj_price'])
            
            # Get inventory
            try:
                inventory_data = api.get_product_inventory(self.cj_product_id, self.cj_variant_id)
                if inventory_data:
                    update_vals['cj_stock_qty'] = int(inventory_data.get('quantity', 0))
            except Exception as e:
                _logger.warning(f"Failed to get inventory for {self.cj_product_id}: {str(e)}")
            
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
                    'title': _('Success'),
                    'message': _('Product synced successfully'),
                    'type': 'success',
                }
            }
        except Exception as e:
            _logger.error(f"Failed to sync product {self.cj_product_id}: {str(e)}")
            raise UserError(_('Failed to sync product: %s') % str(e))
    
    def action_bulk_create_products(self):
        """Create Odoo products for multiple CJ products"""
        for record in self:
            if not record.product_tmpl_id:
                record.action_create_odoo_product()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('%d products created successfully') % len(self),
                'type': 'success',
            }
        }
