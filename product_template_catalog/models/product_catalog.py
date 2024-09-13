from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"
    
    @api.model
    def product_attribute_lines(self):      
        product_template_id = self.id
        
        attribute_lines = self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', product_template_id)
        ])
        
        if attribute_lines:
            _logger.info(len(attribute_lines))
        
        # product_variants = self.env['product.product'].search([
        #     ('product_tmpl_id', '=', product_template_id)
        # ])
        
        
        
        # if product_variants:
        #     variantes = product_variants.product_template
            
        #     _logger.info('')
        
        name = self.name
        
        return name

