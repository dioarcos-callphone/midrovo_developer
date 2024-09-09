from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self, product_template):
        data = []
        product_variants = []
        colores = []

        product_product = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)])
                
        product_attributte_lines = self.env['product.template.attribute.line'].search([(
            'product_tmpl_id', '=', product_template.id
        )])
        
        for product_line in product_attributte_lines:
            color = product_line.attribute_id.name
            if(color.lower() == 'color'):
                for value in product_line.value_ids:
                    colores.append(value.name)
                    
        for color in colores:
            image = ''
            product_variants.clear()
            for product in product_product:
                values = product.product_template_variant_value_ids
                for value in values:
                    val = value.name
                    if(color == val):
                        product_variants.append(product)

                image = product.image_1920
                        
            product_data = {
                "color": color,
                "img": image,
                "data": product_variants
            }
            
            data.append(product_data)
                        
        return data