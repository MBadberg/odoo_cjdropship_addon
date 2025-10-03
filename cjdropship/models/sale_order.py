# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    is_cjdropship_order = fields.Boolean(string='Is CJDropshipping Order',
        compute='_compute_is_cjdropship_order', store=True)
    cjdropship_order_id = fields.Many2one('cjdropship.order', string='CJ Order',
        readonly=True, copy=False)
    cjdropship_state = fields.Selection(related='cjdropship_order_id.state',
        string='CJ Status', readonly=True)
    
    @api.depends('order_line.product_id.is_cjdropship')
    def _compute_is_cjdropship_order(self):
        """Check if order contains CJDropshipping products"""
        for order in self:
            order.is_cjdropship_order = any(
                line.product_id.is_cjdropship for line in order.order_line
            )
    
    def action_confirm(self):
        """Override to auto-submit to CJDropshipping if enabled"""
        res = super(SaleOrder, self).action_confirm()
        
        for order in self:
            if order.is_cjdropship_order and not order.cjdropship_order_id:
                try:
                    config = self.env['cjdropship.config'].get_default_config()
                    if config.auto_fulfill_orders:
                        order._create_cjdropship_order()
                except Exception as e:
                    _logger.warning(f"Failed to auto-submit order {order.name} to CJDropshipping: {str(e)}")
        
        return res
    
    def _create_cjdropship_order(self):
        """Create CJDropshipping order"""
        self.ensure_one()
        
        if self.cjdropship_order_id:
            return self.cjdropship_order_id
        
        config = self.env['cjdropship.config'].get_default_config()
        
        # Create CJ order record
        cj_order = self.env['cjdropship.order'].create({
            'sale_order_id': self.id,
            'config_id': config.id,
        })
        
        self.cjdropship_order_id = cj_order.id
        
        # Auto-submit if configured
        if config.auto_fulfill_orders:
            try:
                cj_order.action_submit_to_cj()
            except Exception as e:
                _logger.error(f"Failed to submit order to CJDropshipping: {str(e)}")
                self.message_post(
                    body=_('Failed to submit order to CJDropshipping: %s') % str(e),
                    message_type='notification'
                )
        
        return cj_order
    
    def action_submit_to_cjdropship(self):
        """Manually submit order to CJDropshipping"""
        self.ensure_one()
        
        if not self.is_cjdropship_order:
            raise UserError(_('This order does not contain CJDropshipping products'))
        
        if not self.cjdropship_order_id:
            self._create_cjdropship_order()
        else:
            self.cjdropship_order_id.action_submit_to_cj()
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cjdropship.order',
            'res_id': self.cjdropship_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_view_cjdropship_order(self):
        """View CJDropshipping order"""
        self.ensure_one()
        
        if not self.cjdropship_order_id:
            raise UserError(_('No CJDropshipping order found'))
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cjdropship.order',
            'res_id': self.cjdropship_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
