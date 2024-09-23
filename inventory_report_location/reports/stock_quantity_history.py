from odoo import api, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class StockQuantityHistory(models.AbstractModel):
    _name = 'report.inventory_report_location.report_stock_quantity'
    _description = 'Stock Quantity History'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        location_id = [ data['location_id'] if data.get('location_id') else 8, 18 ]
        
        _logger.info(f'LOCATION ID >>>> { location_id }')
        
        domain = [
            ('location_id', 'in', location_id),
            ('inventory_date', '!=', False)
        ]
        
        # Agrupamos por el nombre del producto y el precio estándar
        quant_records = self.env['stock.quant'].read_group(
            domain,
            ['product_id', 'quantity'],
            ['product_id',],
        )
        
        _logger.info(f'MOSTRANDO RESULTADO >>> { quant_records }') 

        # Procesamos los resultados
        result = []
        for record in quant_records:
            result.append({
                'name': self.env['product.product'].browse(record.get('product_id')[0]).product_tmpl_id.name,  # Nombre del producto
                'costo': record.get('quantity'),    # Precio estándar
                'cantidad': record.get('quantity'),  # Precio estándar
            })
        
        _logger.info(f'MOSTRANDO RESULTADO >>> { result }') 
        
        if result:          
            return {
                'doc_ids': docids,
                'doc_model': 'report.stock.quantity.history',
                'options': result,
            }
            
        else:
            raise ValidationError("No records found for the given criteria!")
        