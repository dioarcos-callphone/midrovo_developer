from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self):
        data = []
        colores = []
        talla = []

        product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        
        if product_product:        
            product_attributte_lines = self.env['product.template.attribute.line'].search([(
                'product_tmpl_id', '=', self.id
            )])
            
            for product_line in product_attributte_lines:
                color = product_line.attribute_id.name
                if(color.lower() == 'color'):
                    for value in product_line.value_ids:
                        colores.append(value.name)
                        
                if(color.lower() == 'talla' or color.lower() == 'tallas'):
                    for value in product_line.value_ids:
                        talla.append(value.name)
                        
            if not colores:
                return None 
            
            if not talla:
                return None           
            
            for color in colores:
                suma_disponible = 0
                product_variants = []
                for product in product_product:
                    values = product.product_template_variant_value_ids
                    
                    if(values):
                        if(len(values) > 1):
                            for value in values:
                                val = value.name
                                if(color == val):
                                    suma_disponible += int(product.qty_available)
                                    
                                    product_variants.append(product)
                                    
                        else:
                            val = values.name
                            if(color == val):
                                suma_disponible += int(product.qty_available)
                                
                                product_variants.append(product)
                                
                            elif(values.attribute_id.name.lower() == 'tallas' or values.attribute_id.name.lower() == 'talla'):
                                suma_disponible += int(product.qty_available)
                                
                                product_variants.append(product)
                                
                    else:
                        suma_disponible += int(product.qty_available)
                        product_variants.append(product)

                product_data = {
                    "color": color,
                    "img": product_variants[0].id,
                    "tallas": product_variants,
                    "disponible": suma_disponible,
                    "talla_unica": talla
                }

                data.append(product_data)
                        
            return data
        
        return None