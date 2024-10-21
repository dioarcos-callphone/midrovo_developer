# -*- encoding: utf-8 -*-

{
    "name": "Utilidades Varias",
    "version": "1.0",
    "depends": ['base',
                'product',
                'account',
                'mail',
                'web',
                ],
    "author": "",
    "website": "https://",
    "category": "Development Tools",
    "complexity": "normal",
    "description": """
    This module provide :
    Utilidades varias
    """,
    "init_xml": [],
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'data/config_parameters_data.xml',
        'data/notification_data.xml',
        'data/cron_jobs_data.xml',
        'reports/report_template.xml',
        'views/menu_root.xml',
        'views/notification_view.xml',
        'wizard/wizard_produc_no_stock_view.xml',
        'wizard/wizard_product_default_tax_view.xml',
        'wizard/wizard_message_view.xml',
        'views/web_assets.xml',
        'views/res_users_view.xml',
        'views/paperformat.xml'
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
