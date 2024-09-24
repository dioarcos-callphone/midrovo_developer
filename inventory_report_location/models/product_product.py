from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def action_pdf(self):
        data_productos = []
        
        for producto in self:
            variantes = []
            data = {
                # "id": self.id,
                "nombre": self.name,
                "cantidad": self.qty_quantity,
                "costo": self.standard_price,
            }
            
            if producto.product_template_variant_value_ids:
                for v in producto.product_template_variant_value_ids:
                    variantes.append({
                        f'{ v.attribute_id.name }' : f'{ v.name }',
                    })
                    
                data['atributos'] = variantes
                
            data_productos.append(data)
            
        _logger.info(f'MOSTRANDO PRODUCTOS >>> { data_productos }')
            
        
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(None, data=data_productos)
        )