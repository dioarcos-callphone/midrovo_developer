from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self, product_template_id):
        product_variants = self.env['product.product'].search([('id', '=', product_template_id)])
        
        data = []
        
        for product_variant in product_variants:
            data.append(product_variant)
            
            
        return data