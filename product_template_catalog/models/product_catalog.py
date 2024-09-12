from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"
    
    @api.model
    def product_catalog_group_by_dinamic(self):
        product_tmpl_attribute_lines = self.env['product.template.attribute_line'].search([('product_tmpl_id','=',self.id)])
        
        _logger.info('YYYY MOSTRANDO VALOR YYYY')
        _logger.info(product_tmpl_attribute_lines)
        
        return self.name