from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"
    
    @api.model
    def product_attribute_lines(self):      
        product_template_id = self.id
        
        attribute_lines = self.env['product.template.attribute.line'].search_read([
            ('product_tmpl_id', '=', product_template_id)
        ])
        
        if attribute_lines:
            _logger.info(len(attribute_lines))
        
        name = self.name
        
        return name
    
    @api.model
    def product_variant_group(self):
        product_id = self.id
        
        attributes = self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', product_id),
            ('attribute_id.name', 'in', ['color', 'tallas'])
        ])
        
        if attributes:
            
            for a in attributes:
                _logger.info(f'ATTT >>> { a.value_ids }')
            
            variant_values = [v_val.id for v_id in attributes for v_val in v_id.value_ids]
        
            _logger.info(f'Mostrando atributos >>> { variant_values } ')
            
            product_variants = self.env['product.product'].read_group(
                domain=[
                    ('product_tmpl_id', '=', product_id),
                    ('product_template_variant_value_ids', 'in', variant_values)
                ],
                fields=['product_template_variant_value_ids'],
                groupby=[
                    'product_template_variant_value_ids',
                ],
                lazy=False
            )
            
            formatted_variants = []
            for variant in product_variants:
                d = variant['product_template_variant_value_ids']
                
                _logger.info(f'PRODUCT TEMPLATE VARIANT VALUE IDS >>> { d }')
                
                value = self.env['product.template.attribute.value'].browse(variant['product_template_variant_value_ids'][0])
                
                _logger.info(f'VALUES >>> { value.product_attribute_value_id }')
                
                
                if value.product_attribute_value_id.id in variant_values:
                    formatted_variants.append({
                        'variante': value.name,
                        'count': variant['__count'],
                    })
            
            _logger.info(formatted_variants)
        
        return 'prueba'

