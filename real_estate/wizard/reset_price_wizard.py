# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResetPriceWizard(models.Model):
    _name = 'reset.price.wizard'
    _description = 'Reset Price'

    customers = fields.Many2many(
        string='Customers', comodel_name='property.customer', required=True,
        default=lambda self: self._context.get('default_customers')
    )

    def action_reset_price(self):
        self.customers.with_context(do_reset=True).action_reset_price()

