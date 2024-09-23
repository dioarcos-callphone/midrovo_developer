from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)



class StockQuantityHistoryInherit(models.TransientModel):
    _inherit = 'stock.quantity.history'
    
    categ_ids = fields.Many2many('product.category', string='Categorías')
    
    def action_pdf(self):        
        """This function is for printing pdf report"""
        data = {
            'model_id': self.id,
            'location_id': self.location_id.id,
            'category_ids': self.categ_ids.ids,
            'date': self.inventory_datetime
        }
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(None, data=data))