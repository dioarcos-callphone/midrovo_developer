from odoo import api, models
from odoo.exceptions import ValidationError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class StockQuantityHistory(models.AbstractModel):
    _name = 'report.inventory_report_location.report_stock_quantity'
    _description = 'Stock Quantity History'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        productos = data['productos']
        localidad_fecha = ''
        
        locations = self.env.context.get('location',[])
        fecha = self.env.context.get('date',[])
        
        _logger.info(f'fecha >> { fecha }')
        
        for location in locations:
            localidad_fecha = localidad_fecha + " " + location
            
        localidad_fecha += fecha     
        
        
            
        if productos:
            return {
                'doc_ids': docids,
                'doc_model': 'report.stock.quantity.history',
                'options': productos,
                'total_cantidad': data['total_cantidad'],
                "total_valor_stock" : data['total_valor_stock'],
                'localidad_fecha': localidad_fecha
            }
            
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")
                