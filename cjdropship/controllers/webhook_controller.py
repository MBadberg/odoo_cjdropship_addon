# -*- coding: utf-8 -*-

import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CJDropshippingWebhookController(http.Controller):
    
    @http.route('/cjdropship/webhook/<int:config_id>', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_webhook(self, config_id, **kwargs):
        """Receive webhook from CJDropshipping"""
        try:
            # Get config to verify it exists
            config = request.env['cjdropship.config'].sudo().browse(config_id)
            if not config.exists() or not config.webhook_enabled:
                return {'status': 'error', 'message': 'Webhook not enabled'}
            
            # Get request data
            payload = request.httprequest.get_json(force=True)
            headers = dict(request.httprequest.headers)
            
            # Determine webhook type
            webhook_type = 'other'
            event = payload.get('event', '')
            
            if 'order' in event.lower() and 'status' in event.lower():
                webhook_type = 'order_status'
            elif 'tracking' in event.lower():
                webhook_type = 'tracking'
            elif 'inventory' in event.lower() or 'stock' in event.lower():
                webhook_type = 'inventory'
            
            # Create webhook record
            webhook = request.env['cjdropship.webhook'].sudo().create({
                'webhook_type': webhook_type,
                'cj_order_id': payload.get('orderId', ''),
                'event': event,
                'payload': json.dumps(payload, indent=2),
                'headers': json.dumps(headers, indent=2),
            })
            
            # Process webhook immediately
            webhook.action_process_webhook()
            
            _logger.info(f"Received CJDropshipping webhook: {event}")
            
            return {'status': 'success', 'message': 'Webhook received'}
            
        except Exception as e:
            _logger.error(f"Error processing CJDropshipping webhook: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    @http.route('/cjdropship/webhook/test', type='http', auth='public', methods=['GET'])
    def test_webhook(self, **kwargs):
        """Test endpoint to verify webhook URL is accessible"""
        return "CJDropshipping webhook endpoint is active"
