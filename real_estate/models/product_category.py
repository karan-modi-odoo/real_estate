# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    commission_percentage = fields.Float(string='Commission Percentage')
