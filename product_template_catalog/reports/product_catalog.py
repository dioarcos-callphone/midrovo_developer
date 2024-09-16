from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"
    
    @api.model
    def product_variant_group(self):
        products_data = []
        product_id = self.id
        
        attributes = self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', product_id),
            ('attribute_id.name', 'in', ['color', 'tallas'])
        ])
        
        if attributes:
            attribute_lines = [ a.id for a in attributes ]
            values_attributes = self.env['product.template.attribute.value'].search([('attribute_line_id', 'in', attribute_lines)])
            values_attributes_ids = [ v.id for v in values_attributes ]
             
            variant_values = [v_val.id for v_id in attributes for v_val in v_id.value_ids]
                 
            product_variants = self.env['product.product'].read_group(
                domain=[
                    ('product_tmpl_id', '=', product_id),
                    ('product_template_variant_value_ids', 'in', values_attributes_ids)
                ],
                fields=['product_template_variant_value_ids'],
                groupby=[
                    'product_template_variant_value_ids',
                ],
                lazy=False
            )
            
            formatted_variants = []
            for variant in product_variants:                
                value = self.env['product.template.attribute.value'].browse(variant['product_template_variant_value_ids'][0])
                
                if value.product_attribute_value_id.id in variant_values:
                    formatted_variants.append({
                        'variante': value.name,
                        'count': variant['__count'],
                    })
            
            products = self.env['product.product'].search([
                    ('product_tmpl_id', '=', product_id),
                    ('product_template_variant_value_ids', 'not in', values_attributes_ids)
            ])
            
            mi_set = set(products)
            
            for p in mi_set:
                _logger.info(p.product_template_variant_value_ids)
            
            _logger.info(formatted_variants)
            
            # for p in products:
            #     vals_variant = []
            #     variantes = p.product_template_variant_value_ids
                
            #     if variantes:
            #         for v in variantes:
            #             vals_variant.append(v.name)
                        
            #     else:
            #         vals_variant.append('no hay valores de variante')
                
            #     data = {
            #         'name': p.name,
            #         'variants': vals_variant
            #     }
                
            #     products_data.append(data)
            #     _logger.info(f'MOSTRANDO PRODUCT PRODUCT { p.product_template_variant_value_ids }')
        
        # return products_data or [{ 'name': 'no variant', 'variants': ['no hay valores de variante'] }]
        
        return 'prueba'

