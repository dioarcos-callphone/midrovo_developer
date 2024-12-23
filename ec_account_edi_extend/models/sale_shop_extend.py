from odoo import models, fields

class SaleShopExtend(models.Model):
    _inherit = 'sale.shop'
    _description = 'Establecimientos'
    
    name = fields.Char(
        u'Nombre de Establecimiento',
        size=256,
        required=True,
        readonly=False,
        index=True, 
    )
    