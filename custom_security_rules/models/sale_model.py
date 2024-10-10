from odoo import models, fields, api

class SaleModel(models.Model):
    _inherit = 'sale.order'
    
    user_id = fields.Many2one(
        comodel_name='res_users'
    )