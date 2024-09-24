from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def action_pdf(self):
        data_productos = []
        
        for producto in self:
            variantes = []
            
            if producto.qty_available > 0 and producto.standard_price > 0 and producto.total_value > 0:
                data = {
                    "id": producto.id,
                    "nombre": producto.name,
                    "cantidad": producto.qty_available,
                    "costo": round(int(producto.standard_price), 3),
                    "valor_stock": round(int(producto.total_value), 3),
                }
            
                if producto.product_template_variant_value_ids:
                    for v in producto.product_template_variant_value_ids:
                        variantes.append({
                            f'{ v.attribute_id.name }' : f'{ v.name }',
                        })
                    
                data['atributos'] = variantes
                
            data_productos.append(data)
            
        data = {
            "productos" : data_productos
        }
        
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(None, data=data)
        )