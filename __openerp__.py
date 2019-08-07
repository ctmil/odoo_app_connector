# -*- coding: utf-8 -*-
{
    'name': "Odoo App Connector",

    'summary': """
        Connector for Odoo App in Community version.""",

    'description': """
        Connector for Odoo App in Community version.
    """,

    'author': "Moldeo Interactive",
    'website': "https://www.moldeointeractive.com.ar",

    'category': 'Web',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ]
}
