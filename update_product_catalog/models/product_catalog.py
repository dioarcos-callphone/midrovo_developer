from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self):
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
            for product in product_product:
                values = product.product_template_variant_value_ids
                for value in values:
                    val = value.name
                    if(color == val):
                        _logger.info(f'MOSTRANDO COLOR >>> { val }')
                        _logger.info(f'MOSTRANDO CANTIDAD DISPONIBLE >>> { product.immediately_usable_qty }')
                        product_variants.append(product)
                        
            variantes = product_variants
            product_variants.clear()

            product_data = {
                "color": color,
                "img": product_variants[0].id,
                "tallas": variantes
            }

            data.append(product_data)
            
        for r in data:
            for talla in r['tallas']:
                _logger.info(f'CANTIDAD DISPONIBLE >>> { talla.immediately_usable_qty }')
                        
        return data