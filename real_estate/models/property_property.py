# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request

class PropertyProperty(models.Model):
    _name = 'property.property'
    _description = 'Property'

    name = fields.Char(string='Name', default="New", readonly=True)
    type = fields.Selection([
        ('bungalow', 'Bungalow'),
        ('flat', 'Flat'),
        ('apartment', 'Apartment'),
    ], string='Type', required=True)
    floor = fields.Integer(string='Floor')
    customer = fields.Many2one(
        string='Customer',
        comodel_name="property.customer"
    )
    email = fields.Char(related="customer.email", readonly=False, store=True)
    address = fields.Text(string='Address')
    resell = fields.Boolean(string='Resell', default=False)
    image = fields.Binary(string="Image")
    age = fields.Integer(string="Age")
    price = fields.Float(string="Price")
    register_date= fields.Date(string="Register Date")
    description = fields.Html(string="Description")
    elevator = fields.Boolean(string="Elevator")
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    area = fields.Float(string="Area", compute='_compute_area', store=True)
    property_count = fields.Integer(string="Property Count")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sold', 'Sold'),
    ], string='State', default='draft')
    sales_person = fields.Many2many(
        string="Sales Person",
        comodel_name="res.partner",
        relation="property_property_sales_person_rel",
        column1="property_id",
        column2="sales_person_id"
    )

    def action_mark_sold(self):
        template = request.env.ref('real_estate.mail_template_property_sold', raise_if_not_found=False)
        for rec in self:
            rec.state = 'sold'
            template.sudo().send_mail(rec.id, force_send=True)

    @api.onchange('type')
    def _onchange_type(self):
        if self.type == 'flat':
            self.elevator = True
        else:
            self.elevator = False

    @api.depends('height', 'width')
    def _compute_area(self):
        print("\n\n", self)
        for rec in self:
            rec.area = rec.height * rec.width

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('property.property')
        return super().create(vals_list)


