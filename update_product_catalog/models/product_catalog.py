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
        # product_variants = self.search([('atrribute_id', '=', product_template.attribute_id)],)
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
            for product in product_product:
                values = product.product_template_variant_value_ids
                for value in values:
                    color = value.name
                    if(color == color):
                        product_variants.append(product)
                        _logger.info(f'VALORES >>> { color }')
                        
            product_data = {
                "color": color,
                "data": product_variants
            }
            
            data.append(product_data)
            
            product_variants.clear()
            
        
        
        _logger.info(f'MOSTRANDO PRODUCT PRODUCT >>> { product_product }')
        _logger.info(f'MOSTRANDO PRODUCT DATA >>> { product_data }')
        
        # product_attributte_lines = self.env['product.template.attribute.line'].search([(
        #     'product_tmpl_id', '=', product_template.id
        # )])
        
        # _logger.info(f'PRODUCTO TEMPLATE >>> { product_attributte_lines.value_ids }')
        
        # for product_line in product_attributte_lines:
        #     color = product_line.attribute_id.name
        #     if(color.lower() == 'color'):
        #         for value in product_line.value_ids:
        #             _logger.info(f'MOSTRANDO COLORES >>> { value.name }')
        
        # variantes = []
        
        # for product_variant in product_variants:
        #     # variant_values = product_variant.product_template_variant_value_ids
            
        #     # for variant_value in variant_values:
        #     #     _logger.info(f'MOSTRANDO VARIANT VALUE >>> { variant_value.product_attribute_value_id.name }')
            
        #     _logger.info(f'MOSTRANDO LA DATA >>> { product_variant.product_template_variant_value_ids.attribute_id }')
            
        #     variantes.append(product_variant.product_template_variant_value_ids.attribute_id)
                        
        return 'variantes'