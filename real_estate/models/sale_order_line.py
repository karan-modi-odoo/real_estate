# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    commission_rate=fields.Float(string="Commission Rate", compute="_compute_commission_rate", store=True)
    line_commission_amount = fields.Float(
        string="Line Commission Amount", compute="_compute_line_commission_amount", store=True
    )

    @api.depends('product_id.categ_id.commission_percentage')
    def _compute_commission_rate(self):
        for rec in self:
            rec.commission_rate = rec.product_id.categ_id.commission_percentage


    @api.depends('commission_rate', 'price_subtotal')
    def _compute_line_commission_amount(self):
        for rec in self:
            rec.line_commission_amount = rec.price_subtotal * rec.commission_rate / 100

    @api.model_create_multi
    def create(self, vals_list):
        print("\n\nSOL create context>>>>>>>>>>", self._context)
        for vals in vals_list:
            if self._context.get('from_add_product'):
                vals['product_uom_qty'] = 5

        return super(SaleOrderLine, self).create(vals_list)