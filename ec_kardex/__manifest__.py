# -*- coding: UTF-8 -*- #

{
    "name" : "KARDEX",
    "version" : "1.0",
    "author" : "",

    "depends" : [
        'stock_account',
        'purchase',
        'ec_tools'
    ],
    "init": [],
    "data": [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'views/menu_root.xml',
        'views/stock_valuation_layer_view.xml',
        'views/product_template_views.xml',
        'views/kardex_report_reg_views.xml',
        'reports/report_kardex_all.xml',
        'reports/report_kardex_individual.xml',
        'reports/stock_reports.xml',
        'reports/report_kardex_all_stock.xml',
        'wizard/wizard_kardex_all_view.xml',
        'wizard/wizard_kardex_individual_view.xml',
        'wizard/wizard_kardex_all_stock_view.xml',
    ],
    
    "installable": True,
    "active": False,
    'license': 'LGPL-3',
}


