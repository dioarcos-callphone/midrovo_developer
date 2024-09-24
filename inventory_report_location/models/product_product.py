from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def action_pdf(self):
        data = {
            "products": self
        }
        
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(None, data=data)
        )