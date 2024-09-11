from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self):
        data = []
        colores = []

        product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        
        _logger.info(f'MOSTRANDO PRODUCTOS >>> { product_product }')
        
        if product_product and len(product_product) > 1:        
            product_attributte_lines = self.env['product.template.attribute.line'].search([(
                'product_tmpl_id', '=', self.id
            )])
            
            for product_line in product_attributte_lines:
                color = product_line.attribute_id.name
                if(color.lower() == 'color'):
                    for value in product_line.value_ids:
                        colores.append(value.name)
                        
            for color in colores:
                suma_disponible = 0
                product_variants = []
                for product in product_product:
                    values = product.product_template_variant_value_ids
                    _logger.info(f'MOSTRANDO VALUES { values }')
                    if(len(values) > 1):
                        for value in values:
                            val = value.name
                            if(color == val):
                                suma_disponible += int(product.immediately_usable_qty)
                                _logger.info('ENTRA AQUI')
                                product_variants.append(product)
                                
                    else:
                        if(values.attribute_id.name.lower() == 'tallas' or values.attribute_id.name.lower() == 'talla'):
                            suma_disponible += int(product.immediately_usable_qty)
                            product_variants.append(product)

                product_data = {
                    "color": color,
                    "img": product_variants[0].id,
                    "tallas": product_variants,
                    "disponible": suma_disponible,
                }

                data.append(product_data)
                        
            return data
        
        return None