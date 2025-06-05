from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def action_pdf(self):
        data_productos = []
        
        total_cantidad = 0
        total_valor_stock = 0 
        
        for producto in self:
            
            variantes = []
            cantidad = producto.qty_available
            cantidad_sin_reserva = producto.immediately_usable_qty
            
            costo = round(producto.standard_price, 3)
            valor_stock = round((costo * cantidad), 3)
            
            total_cantidad += cantidad
            total_valor_stock += valor_stock

            data = {
                "id": producto.id,
                "nombre": producto.name,
                "cantidad": cantidad,
                "cantidad_sin_reserva": cantidad_sin_reserva,
                "costo": costo,
                "valor_stock": valor_stock,
            }
        
            if producto.product_template_variant_value_ids:
                for v in producto.product_template_variant_value_ids:
                    variantes.append({
                        f'{ v.attribute_id.name }' : f'{ v.name }',
                    })
                
            data['atributos'] = variantes
            data_productos.append(data)
            
        data = {
            "productos" : data_productos,
            "total_cantidad" : total_cantidad,
            "total_valor_stock" : round(total_valor_stock, 3),
        }
        
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(self, data=data)
        )
        