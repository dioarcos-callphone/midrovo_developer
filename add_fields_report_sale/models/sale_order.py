from odoo import _, api, fields, models

class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'
    
    report_grids = fields.Boolean(string="Print Variant Grids", default=False)

    def get_report_matrixes(self):
        result = super(SaleOrderExtend, self).get_report_matrixes()
        
        result = []
        
        return result 
