from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self, product_template_id):
        product_variants = self.env['product.product'].search([('product_tmpl_id', '=', product_template_id)])
        
        data = []
        
        for product_variant in product_variants:
            data.append(product_variant)
            
        _logger.info(f'MOSTRANDO LA DATA >>> { data }')
            
        return data