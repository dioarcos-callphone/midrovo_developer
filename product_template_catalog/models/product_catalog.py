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
        
        attributes = self.env['product.template.attribute.value'].search([
            ('product_tmpl_id', '=', product_id),
            ('attribute_id.name', 'in', ['color', 'tallas'])
        ])
        
        if attributes:
            attribute_ids = [ a.id for a in attributes ]
        
            _logger.info(f'Mostrando atributos >>> { attributes } ')
            
            product_variants = self.env['product.product'].read_group(
                domain=[
                    ('product_tmpl_id', '=', product_id),
                    ('product_template_variant_value_ids', 'in', attribute_ids )
                ],
                fields=['product_template_variant_value_ids'],
                groupby=[
                    'product_template_variant_value_ids',
                ],
                lazy=False
            )
            
            _logger.info(f'Mostrando variantes de producto >>> { product_variants }')
            
            formatted_variants = []
            for variant in product_variants:
                variant_values = self.env['product.template.attribute.value'].browse(variant['product_template_variant_value_ids'][0])
                
                # attribute = variant_values.attribute_id.name
                
                # if attribute in [ 'tallas', 'color' ]:
                #     formatted_variants.append({
                #         'variante': variant_values.attribute_id.name,
                #         'count': variant['__count'],
                #     })
                
                formatted_variants.append({
                    'variante': variant_values.name,
                    'count': variant['__count'],
                })
            
            _logger.info(formatted_variants)
        
        return 'prueba'

