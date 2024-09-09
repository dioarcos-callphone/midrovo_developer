from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self):
        _logger.info(f'MOSTRANDO PRODUCT TEMPLATE >>> { self.id }')
        data = []
        product_variants = []
        colores = []

        product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
                
        product_attributte_lines = self.env['product.template.attribute.line'].search([(
            'product_tmpl_id', '=', self.id
        )])
        
        for product_line in product_attributte_lines:
            color = product_line.attribute_id.name
            if(color.lower() == 'color'):
                for value in product_line.value_ids:
                    colores.append(value.name)
                    
        for color in colores:
            product_variants.clear()
            for product in product_product:
                values = product.product_template_variant_value_ids
                for value in values:
                    val = value.name
                    if(color == val):
                        product_variants.append(product)

            product_data = {
                "color": color,
                "img": product_variants[0].id,
                "data": product_variants
            }
            
            data.append(product_data)
                        
        return data