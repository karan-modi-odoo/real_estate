# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    gst_no = fields.Char(string='GST', tracking=True, copy=False)
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    full_name = fields.Char(string='Full Name')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals["first_name"] and vals["last_name"]:
                vals["full_name"] = vals["first_name"] + " " + vals["last_name"]

            elif vals["full_name"]:
                part = vals["full_name"].split(" ", 1)
                vals["first_name"] = part[0]
                vals["last_name"] = part[1]

        return super().create(vals_list)

    def write(self, vals):
        print("\nself", self)
        print("\nvals", vals)
        if "first_name" in vals and "last_name" in vals:
            vals["full_name"] = vals["first_name"] + " " + vals["last_name"]

        elif vals.get("full_name", False):
            part = vals["full_name"].split(" ", 1)
            vals["first_name"] = part[0]
            vals["last_name"] = part[1]

        return super().write(vals)

    @api.depends('phone')
    def _compute_display_name(self):
        super()._compute_display_name()
        for rec in self:
            rec.display_name = (rec.name + ' | ' + rec.phone) if rec.phone else rec.name

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = list(args or [])
        if not name:
            # When no name is provided, call the parent implementation
            return super().name_search(name=name, args=args, operator=operator,
                                       limit=limit)
        # Add search criteria for name, email, and phone
        domain = ['|',
                  ('name', operator, name),
                  ('phone', operator, name)
                  ]
        # Combine with existing args
        if args:
            domain = ['&'] + args + domain
        # Use search_fetch to get both IDs and display_name efficiently
        partners = self.search_fetch(domain, ['display_name'], limit=limit)
        # Return in the expected format: [(id, display_name), ...]
        return [(partner.id, partner.display_name) for partner in partners]