from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self):
        data_catalog = []
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
                                    if product.immediately_usable_qty > 0:
                                        suma_disponible += int(product.immediately_usable_qty)
                                        product_variants.append(product)
                                    
                        else:
                            val = values.name
                            if(color == val):
                                if product.immediately_usable_qty > 0:
                                    suma_disponible += int(product.immediately_usable_qty)
                                    product_variants.append(product)
                                
                            elif(values.attribute_id.name.lower() == 'tallas' or values.attribute_id.name.lower() == 'talla'):
                                if product.immediately_usable_qty > 0:
                                    suma_disponible += int(product.immediately_usable_qty)
                                    product_variants.append(product)
                                
                    else:
                        if product.immediately_usable_qty > 0:
                            suma_disponible += int(product.immediately_usable_qty)
                            product_variants.append(product)

                product_data = {
                    "color": color,
                    "img": product_variants[0].id,
                    "tallas": product_variants,
                    "disponible": suma_disponible,
                    "talla_unica": talla
                }

                data.append(product_data)
                        
            # return data
        if data:
            for d in data:
                product_catalogo = {}
                col = d['color']
                _logger.info(f'color  >>>>  { col }')
                tallas = d['tallas']
                for ta in talla:
                    for t in tallas:
                        for v in t.product_template_variant_value_ids:
                            if v.attribute_id.name.lower() in ['talla', 'tallas']:
                                if v.name == ta:
                                    _logger.info(f'talla >>> { v.name } - precio >>> { t.immediately_usable_qty }')
                _logger.info(" ")
        return data if data else None