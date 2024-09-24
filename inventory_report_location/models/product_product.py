from odoo import models, fields, api

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def action_pdf(self):
        pass