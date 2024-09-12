from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"
    
    @api.model
    def product_catalog_group_by_dinamic(self):
        product_variants = self.env['product.product'].read_group(
            [ 'product_tmpl_id', 'name', 'product_template_variant_value_ids', 'qty_available', 'immediately_usable_qty' ],
            [ 'product_tmpl_id' ]
        )
        
        for variant in product_variants:
            _logger.info('YYYY MOSTRANDO VALOR YYYY')
            
            name = variant.get('name')
            variant_values = variant.get('product_template_variant_value_ids')
            qty_available = variant.get('qty_available')
            immediately_usable = variant.get('immediately_usable_qty')
            
            _logger.info(f'Nombre del producto: { name }')
            _logger.info(f'Variantes: { variant_values }')
            _logger.info(f'Cantidad en mano: { qty_available }')
            _logger.info(f'Cantidad inmediata: { immediately_usable }')
        
        # _logger.info('YYYY MOSTRANDO VALOR YYYY')
        # _logger.info(product_variants)
        
        name = self.name
        
        return name