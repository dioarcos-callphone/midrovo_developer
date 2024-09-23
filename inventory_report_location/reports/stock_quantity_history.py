from odoo import api, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class StockQuantityHistory(models.AbstractModel):
    _name = 'report.inventory_report_location.report_stock_quantity'
    _description = 'Stock Quantity History'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        date = data.get('date')
        location_id = []
        if data.get('location_id'):
            location_id.append(data['location_id'])
            
        else:
            location_id.append(8)
            location_id.append(18)
        
        _logger.info(f'MOSTRANDO FECHA >>> { date }')
        
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

        # Procesamos los resultados
        result = []
        for record in quant_records:
            producto = self.env['product.product'].browse(record.get('product_id')[0])

            result.append({
                'name': producto.product_tmpl_id.name,  # Nombre del producto
                'costo': producto.standard_price if producto.standard_price else producto.product_tmpl_id.standard_price,  # Precio estándar
                'cantidad': record.get('quantity'),  # Cantidad de stock
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
        