# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from .cjdropship_api import CJDropshippingAPI

_logger = logging.getLogger(__name__)


class CJDropshippingConfig(models.Model):
    _name = 'cjdropship.config'
    _description = 'CJDropshipping Configuration'
    _rec_name = 'name'
    
    name = fields.Char(string='Configuration Name', required=True, default='CJDropshipping Settings')
    active = fields.Boolean(string='Active', default=True)
    
    # API Credentials
    api_email = fields.Char(string='API Email', help="Your CJDropshipping account email")
    api_password = fields.Char(string='API Password', help="Your CJDropshipping account password")
    
    # Sync Settings
    auto_sync_products = fields.Boolean(string='Auto Sync Products', default=False,
        help="Automatically sync product inventory and prices")
    sync_interval = fields.Integer(string='Sync Interval (hours)', default=24,
        help="Interval in hours for automatic product sync")
    
    auto_fulfill_orders = fields.Boolean(string='Auto Fulfill Orders', default=False,
        help="Automatically send orders to CJDropshipping when confirmed")
    
    # Product Settings
    default_product_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')
    ], string='Default Product Type', default='consu', required=True)
    
    default_categ_id = fields.Many2one('product.category', string='Default Product Category',
        help="Default category for imported products")
    
    price_markup_type = fields.Selection([
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage')
    ], string='Price Markup Type', default='percentage')
    
    price_markup = fields.Float(string='Price Markup', default=30.0,
        help="Markup to add to CJDropshipping prices")
    
    # Webhook Settings
    webhook_url = fields.Char(string='Webhook URL', readonly=True, compute='_compute_webhook_url',
        help="URL for CJDropshipping to send status updates")
    webhook_enabled = fields.Boolean(string='Enable Webhooks', default=True)
    
    # Status
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)
    connection_status = fields.Selection([
        ('not_tested', 'Not Tested'),
        ('connected', 'Connected'),
        ('error', 'Connection Error')
    ], string='Connection Status', default='not_tested', readonly=True)
    connection_message = fields.Text(string='Connection Message', readonly=True)
    
    @api.depends('webhook_enabled')
    def _compute_webhook_url(self):
        """Compute webhook URL"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.id:
                record.webhook_url = f"{base_url}/cjdropship/webhook/{record.id}"
            else:
                record.webhook_url = f"{base_url}/cjdropship/webhook/[ID]"
    
    @api.constrains('sync_interval')
    def _check_sync_interval(self):
        """Validate sync interval"""
        for record in self:
            if record.sync_interval < 1:
                raise ValidationError(_('Sync interval must be at least 1 hour'))
    
    @api.constrains('price_markup')
    def _check_price_markup(self):
        """Validate price markup"""
        for record in self:
            if record.price_markup < 0:
                raise ValidationError(_('Price markup cannot be negative'))
    
    def get_api_client(self):
        """Get authenticated API client"""
        self.ensure_one()
        if not self.api_email or not self.api_password:
            raise UserError(_('Please configure API credentials first'))
        
        return CJDropshippingAPI(self.api_email, self.api_password)
    
    def action_test_connection(self):
        """Test API connection"""
        self.ensure_one()
        try:
            api = self.get_api_client()
            # Try to get categories as a test
            api.get_categories()
            
            self.write({
                'connection_status': 'connected',
                'connection_message': 'Connection successful!'
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Successfully connected to CJDropshipping API'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            error_msg = str(e)
            _logger.error(f"CJDropshipping connection test failed: {error_msg}")
            
            self.write({
                'connection_status': 'error',
                'connection_message': error_msg
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Connection Error'),
                    'message': error_msg,
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    def action_sync_products(self):
        """Manually trigger product sync"""
        self.ensure_one()
        if self.connection_status != 'connected':
            raise UserError(_('Please test the connection first'))
        
        # This will be called from the wizard
        action = self.env['ir.actions.actions']._for_xml_id('cjdropship.action_product_import_wizard')
        action['context'] = {'default_config_id': self.id}
        return action
    
    def calculate_sale_price(self, cost_price):
        """Calculate sale price based on markup settings"""
        self.ensure_one()
        if self.price_markup_type == 'percentage':
            return cost_price * (1 + self.price_markup / 100)
        else:
            return cost_price + self.price_markup
    
    @api.model
    def get_default_config(self):
        """Get the default active configuration"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            raise UserError(_('Please configure CJDropshipping settings first'))
        return config
