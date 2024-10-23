# -*- coding: UTF-8 -*- #

{
    "name" : "KARDEX",
    "summary": "Reportes Kardex - Inventario",
    "description": """
    Modulo Ec_Kardex depende de Ec_tools
    Genera reportes kardex

    - Individual por producto
    - General
    - Stock en almacén
    Dirijase al modulo de inventario - informes - reportes kardex

    Los costos no son visibles para el grupo Reportes - Ocultar valores de costo y total costo
    """
    "version" : "1.0",
    "author" : "Mauricio Idrovo",
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
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
    
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
}


