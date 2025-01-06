from odoo import _, api, fields, models

class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'

    def get_report_matrixes(self):
        result = super(SaleOrderExtend, self).get_report_matrixes()
        
        result = []
        
        return result 
