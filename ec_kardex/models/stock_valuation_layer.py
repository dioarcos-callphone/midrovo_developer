from odoo import models, fields


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer' 

    product_type = fields.Selection(related='product_id.type', readonly=True, store=True)