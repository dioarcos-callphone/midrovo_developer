from odoo import api, models
from odoo.exceptions import ValidationError
from datetime import datetime

class StockQuantityHistory(models.AbstractModel):
    _name = 'report.inventory_report_location.report_stock_quantity'
    _description = 'Stock Quantity History'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        productos = data['productos']
            
        if productos:
            return {
                'doc_ids': docids,
                'doc_model': 'report.stock.quantity.history',
                'options': productos,
                'total_cantidad': data['total_cantidad'],
                "total_costo" : data['total_costo'],
                "total_valor_stock" : data['total_valor_stock'],
            }
            
        else:
            raise ValidationError("No records found for the given criteria!")
                