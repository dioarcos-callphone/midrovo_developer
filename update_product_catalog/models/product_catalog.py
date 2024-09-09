from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self, product_template):
        # product_variants = self.search([('atrribute_id', '=', product_template.attribute_id)],)
        
        _logger.info(f'PRODUCTO TEMPLATE >>> { product_template }')
        
        # variantes = []
        
        # for product_variant in product_variants:
        #     # variant_values = product_variant.product_template_variant_value_ids
            
        #     # for variant_value in variant_values:
        #     #     _logger.info(f'MOSTRANDO VARIANT VALUE >>> { variant_value.product_attribute_value_id.name }')
            
        #     _logger.info(f'MOSTRANDO LA DATA >>> { product_variant.product_template_variant_value_ids.attribute_id }')
            
        #     variantes.append(product_variant.product_template_variant_value_ids.attribute_id)
                        
        return 'variantes'