# -*- coding: utf-8 -*-
{
    'name': "balance_portfolio",

    'summary': """
        Saldo de Cartera """,

    'description': """
        Sistema para Relohimsa actualizar cartera.
        Contiene 2 crom para actualizar la cartera.
        Las apis dependen del administrador de apis.
        Crea reglas de grupo que permiten validar al usuario  y el modelo al cual pueden accesar
    """,

    'author': "Callphone",
    'website': "https://www.callphoneecuador.com",

    'category': 'balance_portfolio',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','api_administrator'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/user_profile.xml',
        'views/balance_portfolio.xml',
        'report/balance_portfolio_report.xml',
        'data/cron.xml',
    ],
    # only loaded in demonstration mode
    'images': ['static/description/icon.png'],

}
