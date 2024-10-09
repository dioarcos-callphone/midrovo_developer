from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductCatalog(models.Model):
    _inherit = 'product.template'
    _description = 'Catalogo de Productos'

    def action_product_catalog_pdf(self):
        ids = [ p.id for p in self if p.qty_available > 0 ]
        products = self.get_product_by_ids(ids)
        
        productos = self.get_products_catalog(products)
        _logger.info(f'MOSTRANDO PRODUCTOS >>> { productos }')
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
            ('qty_available', '>', 0)
        ])
        
        if products:            
            return self.get_product_filtered(products)
        
        return None
    
    def get_product_filtered(self, products):
        products_filtered = products.filtered(
            lambda p : 
                any(attr.lower() in ['talla', 'tallas', 'color', 'colores',] for attr in p.product_template_variant_value_ids.mapped('attribute_id.name'))
        )
        
        if products_filtered:
            return [ {
                'name': p.name,
                'color': (
                    next((v.name for v in p.product_template_variant_value_ids
                          if v.attribute_id.name.lower() in ['color', 'colores']), None)
                ),
                'talla': (
                    next((v.name for v in p.product_template_variant_value_ids
                          if v.attribute_id.name.lower() in ['talla', 'tallas']), None)
                ),
                'cantidad': p.qty_available,
                'image': p.image_128 or p.product_tmpl_id.image_128,
            } for p in products_filtered ]
        
        return None
    
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
