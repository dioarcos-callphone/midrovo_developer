from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ProductCatalog(models.Model):
    _inherit = 'product.template'
    _description = 'Catalogo de Productos'

    # Genera la data de los productos que seran mostrados en el catalogo
    def action_product_catalog_pdf(self):
        ids = [ p.id for p in self if p.qty_available > 0 ]  # Obtiene la lista de ids del product.template
        products = self.get_product_by_ids(ids)  # Metodo que filtra los product_product
        
        productos = self.get_products_catalog(products)
            
        data = {
            'productos': productos
        }
        
        return (
            self.env.ref('product_catalog_advanced.report_product_catalog')
            .report_action(self, data=data)
        )
    
    
    def get_product_by_ids(self, ids):
        products = self.env['product.product'].search([
            ('product_tmpl_id', 'in', ids),
            ('qty_available', '>', 0),
            ('product_template_variant_value_ids', '!=', False)
        ])
        
        if products:
                        
            return self.get_product_filtered(products)
        
        raise ValidationError("Este producto no tiene cantidad disponible.")
    
    def get_product_filtered(self, products):
        products_filtered = products.filtered(
            lambda p: any(attr.lower() in ['talla', 'tallas', 'color', 'colores'] for attr in p.product_template_variant_value_ids.mapped('attribute_id.name'))
        )
        
        if products_filtered:
            result = []
            for p in products_filtered:
                # Captura color y talla de product_product
                color = next((v.name for v in p.product_template_variant_value_ids
                            if v.attribute_id.name.lower() in ['color', 'colores']), None)
                talla = next((v.name for v in p.product_template_variant_value_ids
                            if v.attribute_id.name.lower() in ['talla', 'tallas']), None)
                
                # Si no se encontró color o talla en product_product, buscar en attribute_line_ids
                if not color or not talla:
                    for attribute_line in p.product_tmpl_id.attribute_line_ids:
                        for value in attribute_line.value_ids:
                            if not color and attribute_line.attribute_id.name.lower() in ['color', 'colores']:
                                color = value.name
                            if not talla and attribute_line.attribute_id.name.lower() in ['talla', 'tallas']:
                                talla = value.name
                
                result.append({
                    'name': p.name,
                    'color': color,
                    'talla': talla,
                    'cantidad': p.qty_available,
                    'image': p.image_128,
                })
            
            return result
        
        raise ValidationError("Este producto no tiene variantes con color y talla.")
    
    def get_products_catalog(self, products):
        data_products = {}

        for product in products:
            name = product['name']
            color = product['color']
            talla = product['talla']
            cantidad = product['cantidad']
            image = product['image']  # Obtener la imagen del producto

            # Crear la estructura para el producto si no existe
            if name not in data_products:
                data_products[name] = {
                    'name': name,
                    'colores': []
                }

            # Buscar el color en la lista de colores
            color_found = next((color_entry for color_entry in data_products[name]['colores'] if color_entry['color'] == color), None)

            if color_found:
                # Si el color ya existe, buscar la talla
                talla_found = next((talla_entry for talla_entry in color_found['tallas'] if talla_entry['talla'] == talla), None)

                if talla_found:
                    # Si la talla existe, sumar la cantidad
                    talla_found['cantidad'] += cantidad
                else:
                    # Si la talla no existe, agregarla
                    color_found['tallas'].append({
                        'talla': talla,
                        'cantidad': cantidad
                    })
            else:
                # Si el color no existe, agregar un nuevo color con la talla y la imagen
                data_products[name]['colores'].append({
                    'color': color,
                    'image': image,  # Asignar la imagen al color
                    'tallas': [{
                        'talla': talla,
                        'cantidad': cantidad
                    }]
                })

        # Convertir el diccionario a una lista (opcional)
        return list(data_products.values())
