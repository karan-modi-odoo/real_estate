# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyCustomer(models.Model):
    _name = 'property.customer'
    _description = 'Customer'

    name = fields.Char(string='Name', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    image = fields.Binary(string="Image")
    age = fields.Integer(string="Age")
    joining = fields.Date(string="Joining")
    notes = fields.Html(string="Notes")
    property_ids = fields.One2many(string="Properties", comodel_name="property.property", inverse_name="customer")
    property_count = fields.Integer(string="Property Count", compute="_compute_property_count")

    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    def action_view_properties(self):
        action = self.env['ir.actions.act_window']._for_xml_id('real_estate.property_property_main_action')

        if len(self.property_ids) == 1:
            action['res_id'] = self.property_ids[0].id
            action['view_mode'] = 'form'
            action['views'] = []
        else:
            action["domain"] = [("id", "in", self.property_ids.ids)]
        return action

    @api.constrains('phone')
    def _constrains_phone(self):
        for rec in self:
            if len(rec.phone) < 5 or len(rec.phone) > 10:
                raise ValidationError('Phone should contain 5 to 10 digits')

    def action_reset_price(self):
        if not self._context.get('do_reset', False):
            return {
                'type': 'ir.actions.act_window',
                'name': 'Reset Price',
                'res_model': 'reset.price.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_customers': self.ids}
            }

        self.property_ids.price = 0