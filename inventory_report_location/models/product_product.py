from odoo import models, fields, api

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    
    def action_pdf(self):
        data_productos = []
        
        total_cantidad = 0
        total_valor_stock = 0 
        
        for producto in self:
            variantes = []
            cantidad = producto.qty_available
            costo = round(producto.standard_price, 3)
            valor_stock = round(producto.total_value, 3)
            
            total_cantidad += cantidad
            total_valor_stock += valor_stock

            data = {
                "id": producto.id,
                "nombre": producto.name,
                "cantidad": cantidad,
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
            "productos" : data_productos or [{'id': 5, 'nombre': 'name', 'cantidad': 4, 'costo': 5, 'valor_stock': 6}],
            "total_cantidad" : total_cantidad or 1500,
            "total_valor_stock" : round(total_valor_stock, 3) or 3000,
        }
        
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(self, data=data)
        )
        