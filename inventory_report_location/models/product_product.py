from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def action_pdf(self):
        _logger.info(f'MOSTRANDO SELFS >>> { self }')
        
        
    
    
    # def action_pdf(self):        
    #     """This function is for printing pdf report"""
    #     data = {
    #         'model_id': self.id,
    #         'location_id': self.location_ids.ids,
    #         'category_ids': self.category_ids.ids,
    #         'date': self.inventory_datetime
    #     }
    #     return (
    #         self.env.ref('inventory_report_location.report_stock_quantity_history')
    #         .report_action(None, data=data))