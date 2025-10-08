# -*- coding: utf-8 -*-
"""CJDropshipping Order Model."""

import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CJDropshippingOrder(models.Model):
    """Model for CJDropshipping order management."""

    _name = 'cjdropship.order'
    _description = 'CJDropshipping Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'cj_order_id'
    _order = 'create_date desc'

    # CJDropshipping Fields
    cj_order_id = fields.Char('CJ Order ID', index=True)
    cj_order_num = fields.Char('CJ Order Number', readonly=True)

    # Relations
    sale_order_id = fields.Many2one(
        'sale.order',
        'Sale Order',
        required=True,
        ondelete='cascade',
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

    # Order Information
    order_date = fields.Datetime('Order Date', default=fields.Datetime.now)

    # Status
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted to CJ'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
            ('error', 'Error'),
        ],
        'Status',
        default='draft',
        required=True,
        tracking=True
    )

    # Shipping
    tracking_number = fields.Char('Tracking Number', readonly=True)
    shipping_method = fields.Char('Shipping Method')
    shipping_cost = fields.Float('Shipping Cost', digits='Product Price')

    # Logistics
    logistics_info = fields.Text('Logistics Information')
    last_logistics_update = fields.Datetime('Last Logistics Update')

    # Messages
    error_message = fields.Text('Error Message')
    notes = fields.Text('Notes')

    # JSON Data
    request_data = fields.Text('Request Data (JSON)')
    response_data = fields.Text('Response Data (JSON)')

    _sql_constraints = [
        (
            'cj_order_id_unique',
            'unique(cj_order_id)',
            'CJ Order ID must be unique!'
        )
    ]

    def action_submit_to_cj(self):
        """Submit order to CJDropshipping."""
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(
                self.env._('Only draft orders can be submitted')
            )

        if not self.sale_order_id:
            raise UserError(self.env._('Sale order is required'))

        try:
            client = self.config_id.get_api_client()

            # Prepare order data
            order_data = self._prepare_cj_order_data()

            # Store request data
            import json
            self.request_data = json.dumps(order_data, indent=2)

            # Submit to CJDropshipping
            result = client.create_order(order_data)

            # Store response data
            self.response_data = json.dumps(result, indent=2)

            # Update order with CJ order ID
            if result.get('orderId'):
                self.write({
                    'cj_order_id': result['orderId'],
                    'cj_order_num': result.get('orderNum', ''),
                    'state': 'submitted',
                })

                # Update sale order
                self.sale_order_id.message_post(
                    body=self.env._(
                        'Order submitted to CJDropshipping. Order ID: %s'
                    ) % result['orderId']
                )

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': self.env._('Success'),
                        'message': self.env._(
                            'Order submitted successfully. CJ Order ID: %s'
                        ) % result['orderId'],
                        'type': 'success',
                    }
                }
            raise UserError(
                self.env._('Failed to get order ID from CJDropshipping')
            )

        except Exception as exc:
            error_msg = str(exc)
            _logger.error(
                "Failed to submit order to CJDropshipping: %s", error_msg
            )

            self.write({
                'state': 'error',
                'error_message': error_msg,
            })

            raise UserError(
                self.env._('Failed to submit order: %s') % error_msg
            )

    def _prepare_cj_order_data(self):
        """Prepare order data for CJDropshipping API."""
        self.ensure_one()

        order = self.sale_order_id
        partner = order.partner_shipping_id or order.partner_id

        # Prepare order lines
        products = []
        for line in order.order_line:
            if (
                line.product_id.is_cjdropship
                and line.product_id.product_tmpl_id.cjdropship_product_id
            ):
                cj_product = (
                    line.product_id.product_tmpl_id.cjdropship_product_id
                )
                products.append({
                    'productId': cj_product.cj_product_id,
                    'variantId': cj_product.cj_variant_id or '',
                    'quantity': int(line.product_uom_qty),
                })

        if not products:
            raise UserError(
                self.env._(
                    'No CJDropshipping products found in this order'
                )
            )

        # Prepare shipping address
        shipping_address = {
            'country': partner.country_id.code if partner.country_id else '',
            'state': partner.state_id.name if partner.state_id else '',
            'city': partner.city or '',
            'zipCode': partner.zip or '',
            'address': partner.street or '',
            'address2': partner.street2 or '',
            'contactName': partner.name or '',
            'phone': partner.phone or partner.mobile or '',
            'email': partner.email or '',
        }

        # Prepare order data
        order_data = {
            'orderNumber': order.name,
            'products': products,
            'shippingAddress': shipping_address,
            'remark': order.note or '',
        }

        return order_data

    def action_update_status(self):
        """Update order status from CJDropshipping."""
        self.ensure_one()

        if not self.cj_order_id:
            raise UserError(self.env._('CJ Order ID is required'))

        try:
            client = self.config_id.get_api_client()
            result = client.get_order_detail(self.cj_order_id)

            if result:
                self._update_from_cj_data(result)

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': self.env._('Success'),
                        'message': self.env._(
                            'Order status updated successfully'
                        ),
                        'type': 'success',
                    }
                }
        except Exception as exc:
            _logger.error("Failed to update order status: %s", str(exc))
            raise UserError(
                self.env._('Failed to update order status: %s') % str(exc)
            )

    def action_query_logistics(self):
        """Query logistics information."""
        self.ensure_one()

        if not self.cj_order_id:
            raise UserError(self.env._('CJ Order ID is required'))

        try:
            client = self.config_id.get_api_client()
            result = client.query_logistics(self.cj_order_id)

            if result:
                import json
                self.write({
                    'logistics_info': json.dumps(result, indent=2),
                    'last_logistics_update': fields.Datetime.now(),
                })

                # Extract tracking number if available
                if result.get('trackingNumber'):
                    self.tracking_number = result['trackingNumber']

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': self.env._('Success'),
                        'message': self.env._(
                            'Logistics information updated'
                        ),
                        'type': 'success',
                    }
                }
        except Exception as exc:
            _logger.error("Failed to query logistics: %s", str(exc))
            raise UserError(
                self.env._('Failed to query logistics: %s') % str(exc)
            )

    def _update_from_cj_data(self, cj_data):
        """Update order from CJDropshipping data."""
        self.ensure_one()

        # Map CJ status to our status
        status_mapping = {
            'PENDING': 'submitted',
            'PROCESSING': 'processing',
            'SHIPPED': 'shipped',
            'DELIVERED': 'delivered',
            'CANCELLED': 'cancelled',
        }

        cj_status = cj_data.get('status', '').upper()
        new_state = status_mapping.get(cj_status, self.state)

        vals = {
            'state': new_state,
            'tracking_number': cj_data.get('trackingNumber', self.tracking_number),
            'shipping_method': cj_data.get('shippingMethod', self.shipping_method),
        }

        self.write(vals)

        # Post message to sale order
        if self.tracking_number:
            self.sale_order_id.message_post(
                body=_('Tracking number updated: %s') % self.tracking_number
            )
