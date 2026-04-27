# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    big_order = fields.Boolean(string="Big Order", compute="_compute_big_order", store=True)
    original_validity_date = fields.Date(string="Original Validity Date")
    product_variants = fields.Many2one(string="Product Variant", comodel_name="product.product")
    quotation_alert = fields.Selection(
        [
            ('no worries', 'No worries!!'),
            ('expiring soon', 'Expiring soon!!'),
            ('please follow up with customer', 'Please follow up with customer!!'),
            ('expired', 'Expired!!')
        ],
        string="Quotation Alert", compute="_compute_quotation_alert")
    requires_approval = fields.Boolean(string="Require Approval", compute="_compute_requires_approval", store=True)
    is_manager_approved = fields.Boolean(string="Is Manager Approved")
    commission_amount = fields.Float(string="Commission Amount", compute="_compute_commission_amount", store=True)

    @api.depends('order_line', 'order_line.product_uom_qty')
    def _compute_big_order(self):
        for rec in self:
            if (
                    (len(rec.order_line) >= 3 and all(line.product_uom_qty >= 5 for line in rec.order_line))
                    or
                    (len(rec.order_line) < 3 and sum(rec.order_line.mapped('product_uom_qty')) >= 50)
            ):
                rec.big_order = True
                rec.validity_date = (
                        rec.original_validity_date + relativedelta(days=10)
                ) if rec.original_validity_date else False
            else:
                rec.big_order = False

    @api.depends('company_id')
    def _compute_validity_date(self):
        super()._compute_validity_date()
        for rec in self:
            rec.original_validity_date = rec.validity_date

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('validity_date'):
                vals['original_validity_date'] = vals['validity_date']
        return super().create(vals_list)

    def write(self, vals):
        x = self.env['res.partner'].search([])
        return super().write(vals)

    def _compute_quotation_alert(self):
        for rec in self:
            if rec.state in ['draft', 'sent'] and rec.validity_date:
                if ((rec.validity_date - date.today()).days > 10):
                    rec.quotation_alert = 'no worries'
                elif (10 > (rec.validity_date - date.today()).days > 5):
                    rec.quotation_alert = 'expiring soon'
                elif (5 > (rec.validity_date - date.today()).days > 0):
                    rec.quotation_alert = 'please follow up with customer'
                else:
                    rec.quotation_alert = 'expired'
            else:
                rec.quotation_alert = False

    def action_add_product(self):
        print("context>>>>", self._context)
        context = self._context.copy()
        context.update({'from_add_product': True})
        for rec in self:
            if rec.product_variants:
                self.env['sale.order.line'].with_context(context).create({
                    'product_id': rec.product_variants.id,
                    'product_uom_qty': 1,
                    'order_id': rec.id
                })

    @api.depends('amount_total')
    def _compute_requires_approval(self):
        for rec in self:
            if rec.amount_total >= 500:
                rec.requires_approval = True
            else:
                rec.requires_approval = False

    @api.depends('amount_total')
    def _compute_commission_amount(self):
        for rec in self:
            if rec.amount_total:
                rec.commission_amount = rec.amount_total * 0.10

    def action_manager_approve(self):
        for rec in self:
            if rec.requires_approval:
                rec.is_manager_approved = True

    def write(self, vals):
        print("\n\nSO Write vals>>>>>>>>>>", vals)
        if 'amount_total' in vals:

            if vals['amount_total'] >= 500:
                vals['requires_approval'] = True

        if 'state' in vals and vals['state'] == 'sale':
            for rec in self:
                if not rec.is_manager_approved:
                    raise UserError("Please approve the order first")

        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        print("\n\nSO Create vals>>>>>>>>>>", vals_list)
        for vals in vals_list:
            if vals.get('amount_total', 0) >= 500:
                vals['requires_approval'] = True

            if vals.get('state', False) == 'sale':
                for rec in self:
                    if not rec.is_manager_approved:
                        raise UserError("Please approve the order first")

        return super().create(vals_list)

    @api.depends('order_line.line_commission_amount')
    def _compute_commission_amount(self):
        for rec in self:
            rec.commission_amount = sum(rec.order_line.mapped('price_subtotal')) * 0.10

