{
    "name": "Inventory Report Location",
    
    "summary": "Reporte de inventario por Ubicación y Categoria.",
    "description": """
        - Módulo diseñado para Odoo 16 Eterprise
        Muestra el inventario PDF de acuerdo a la categoria de producto y la localidad ademas los valores totales de la cantidad, costo y valor de stock.
        Los usuarios que pertenecen al grupo group_inventory_report_location_user no tienen permitido ver el costo y total costo.
        "
    """,
    
    "category": "Stock",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'stock', 'web' ],
    'data': [
        'security/groups/security_group_data.xml',
        'wizards/stock_quantity_history_wizard.xml',
        'reports/stock_quantity_history_report.xml',
        'reports/stock_quantity_history_template.xml',
        'views/stock_quantity_view.xml',
    ],
    
    # 'assets': {
    #     'web.assets_backend': [
    #         '/inventory_report_location/static/src/js/button_tree_extends.js',
    #         '/inventory_report_location/static/src/xml/button_add_template.xml',
    #     ],
    # },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
