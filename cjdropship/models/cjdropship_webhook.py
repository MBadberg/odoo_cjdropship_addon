# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class CJDropshippingWebhook(models.Model):
    _name = 'cjdropship.webhook'
    _description = 'CJDropshipping Webhook Log'
    _rec_name = 'webhook_type'
    _order = 'create_date desc'
    
    webhook_type = fields.Selection([
        ('order_status', 'Order Status Update'),
        ('tracking', 'Tracking Update'),
        ('inventory', 'Inventory Update'),
        ('other', 'Other'),
    ], string='Webhook Type', required=True)
    
    cj_order_id = fields.Char(string='CJ Order ID', index=True)
    event = fields.Char(string='Event')
    
    # Data
    payload = fields.Text(string='Payload (JSON)')
    headers = fields.Text(string='Headers (JSON)')
    
    # Processing
    processed = fields.Boolean(string='Processed', default=False)
    process_date = fields.Datetime(string='Process Date')
    error_message = fields.Text(string='Error Message')
    
    # Relations
    order_id = fields.Many2one('cjdropship.order', string='CJ Order', ondelete='set null')
    
    def action_process_webhook(self):
        """Process webhook data"""
        self.ensure_one()
        
        if self.processed:
            return
        
        try:
            import json
            payload_data = json.loads(self.payload) if self.payload else {}
            
            if self.webhook_type == 'order_status':
                self._process_order_status_update(payload_data)
            elif self.webhook_type == 'tracking':
                self._process_tracking_update(payload_data)
            elif self.webhook_type == 'inventory':
                self._process_inventory_update(payload_data)
            
            self.write({
                'processed': True,
                'process_date': fields.Datetime.now(),
            })
            
        except Exception as e:
            error_msg = str(e)
            _logger.error(f"Failed to process webhook: {error_msg}")
            self.error_message = error_msg
    
    def _process_order_status_update(self, payload):
        """Process order status update webhook"""
        cj_order_id = payload.get('orderId')
        if not cj_order_id:
            return
        
        # Find corresponding order
        order = self.env['cjdropship.order'].search([
            ('cj_order_id', '=', cj_order_id)
        ], limit=1)
        
        if order:
            order._update_from_cj_data(payload)
            self.order_id = order.id
    
    def _process_tracking_update(self, payload):
        """Process tracking update webhook"""
        cj_order_id = payload.get('orderId')
        tracking_number = payload.get('trackingNumber')
        
        if not cj_order_id:
            return
        
        # Find corresponding order
        order = self.env['cjdropship.order'].search([
            ('cj_order_id', '=', cj_order_id)
        ], limit=1)
        
        if order and tracking_number:
            order.write({
                'tracking_number': tracking_number,
                'state': 'shipped',
            })
            self.order_id = order.id
            
            # Update sale order
            order.sale_order_id.message_post(
                body=_('Tracking number: %s') % tracking_number
            )
    
    def _process_inventory_update(self, payload):
        """Process inventory update webhook"""
        product_id = payload.get('productId')
        quantity = payload.get('quantity')
        
        if not product_id:
            return
        
        # Find corresponding CJ product
        cj_product = self.env['cjdropship.product'].search([
            ('cj_product_id', '=', product_id)
        ], limit=1)
        
        if cj_product and quantity is not None:
            cj_product.write({
                'cj_stock_qty': int(quantity),
                'sync_date': fields.Datetime.now(),
            })
