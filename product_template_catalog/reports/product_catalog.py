from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"
    
    @api.model
    def get_product_variant(self):
        products_data = []
        product_id = self.id
        
        attributes_color = self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', product_id),
            ('attribute_id.name', '=', 'color')
        ])
        
        attributes_talla = self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', product_id),
            ('attribute_id.name', '=', 'tallas')
        ])
        
        if attributes_color and attributes_talla:
            attribute_lines_color = [ a.id for a in attributes_color ]
            attribute_lines_talla = [ a.id for a in attributes_talla ]
            values_attributes_color = self.env['product.template.attribute.value'].search([('attribute_line_id', 'in', attribute_lines_color)])
            values_attributes_talla = self.env['product.template.attribute.value'].search([('attribute_line_id', 'in', attribute_lines_talla)])
            values_attributes_ids_color = [ v.id for v in values_attributes_color ]
            values_attributes_ids_talla = [ v.id for v in values_attributes_talla ]
            
            products = self.env['product.product'].search([
                    ('product_tmpl_id', '=', product_id),
            ])
            
            product_color = []
            product_talla = []
            disponibles =   []
            
            if products:
                for product in products:
                    variants = product.product_template_variant_value_ids
                    
                    product_data = {}
                                        
                    if product.immediately_usable_qty > 0:
                        if variants:
                            for variant in variants:
                                if variant.id in values_attributes_ids_color:
                                    product_color.append(variant.name)
                                    product_data['color'] = variant.name
                                    product_data['imagen'] = product.id
                                
                                if variant.id in values_attributes_ids_talla:                                     
                                    if sum(disponibles) < self.immediately_usable_qty:
                                        product_data['talla'] = variant.name
                                        product_data['disponible'] = product.immediately_usable_qty
                                        product_talla.append({
                                            "talla": variant.name,
                                            "disponible": product.immediately_usable_qty
                                        })
                                        disponibles.append(product.immediately_usable_qty)
                                            
                            if product_data:
                                products_data.append(product_data)
                                
                product_color = set(product_color)
                products_catalog = []
                               
                for color in product_color:
                    producto = {}
                    contador = 0
                    suma = 0
                    if products_data:
                        for product in products_data:
                            if product.get('disponible'):
                                if color == product['color']:
                                    contador = contador + 1
                                    suma = suma + product['disponible']
                                    if contador > 1:
                                        product['disponible'] = suma
                                        producto = product
                                        
                                    else:
                                        producto = product
                            
                    if contador > 1:
                        products_catalog.append(producto)
                    else:
                        products_catalog.append(producto)        
                    
                _logger.info(f'{ products_catalog }')
                              
        return 'prueba'       
