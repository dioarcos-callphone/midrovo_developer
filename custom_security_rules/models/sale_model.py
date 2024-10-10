from odoo import models, fields, api

class SaleModel(models.Model):
    _inherit = 'sale.order'