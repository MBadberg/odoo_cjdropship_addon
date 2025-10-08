# -*- coding: utf-8 -*-
"""CJDropshipping Webhook Model."""

import json
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class CJDropshippingWebhook(models.Model):
    """Model for logging and processing CJDropshipping webhooks."""

    _name = 'cjdropship.webhook'
    _description = 'CJDropshipping Webhook Log'
    _rec_name = 'webhook_type'
    _order = 'create_date desc'

    webhook_type = fields.Selection(
        [
            ('order_status', 'Order Status Update'),
            ('tracking', 'Tracking Update'),
            ('inventory', 'Inventory Update'),
            ('other', 'Other'),
        ],
        required=True
    )

    cj_order_id = fields.Char('CJ Order ID', index=True)
    event = fields.Char()

    # Data
    payload = fields.Text('Payload (JSON)')
    headers = fields.Text('Headers (JSON)')

    # Processing
    processed = fields.Boolean(default=False)
    process_date = fields.Datetime()
    error_message = fields.Text()

    # Relations
    order_id = fields.Many2one(
        'cjdropship.order',
        'CJ Order',
        ondelete='set null'
    )

    def action_process_webhook(self):
        """Process webhook data."""
        self.ensure_one()

        if self.processed:
            return

        try:
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

        except Exception as exc:
            error_msg = str(exc)
            _logger.error("Failed to process webhook: %s", error_msg)
            self.error_message = error_msg

    def _process_order_status_update(self, payload):
        """Process order status update webhook."""
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
        """Process tracking update webhook."""
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
                body=self.env._('Tracking number: %s', tracking_number)
            )

    def _process_inventory_update(self, payload):
        """Process inventory update webhook."""
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
