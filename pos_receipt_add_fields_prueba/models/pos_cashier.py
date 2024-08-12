from odoo import models, fields, api
import logging 

_logger = logging.getLogger(__name__)

class PosCashier(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_invoice_field(self, id):
        res = super(PosCashier, self).get_invoice_field(id)
        
        cashier_name =  res
        
        _logger.info(f'NAME CASHIER >>> { cashier_name }')
        
        # res.update({
            
        # })

        return res