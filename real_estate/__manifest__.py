# -*- coding: utf-8 -*-
{
    'name': "Real Estate Management",
    'summary': "Real Estate Management",
    'description': """Real Estate Management""",
    'author': "Karan",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale_management', 'sale', 'product'],
    'license': 'LGPL-3',
    'data': [
        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'views/property_property_views.xml',
        'views/property_customer_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/product_category_views.xml',
        'wizard/reset_price_wizard_views.xml',
        'data/server_action.xml',
        'data/mail_templates.xml',
        'report/property_customer_report.xml',
        'report/property_customer_templates.xml',
        # 'data/scheduled_action.xml',
        # 'data/automated_action.xml',
    ],
}


