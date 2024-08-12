from odoo import models, field, api
import logging 

_logger = logging.getLogger(__name__)

class PosCashier(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_invoice_field(self, id):
        res = super(PosCashier, self).get_invoice_field(id)
        
        cashier_name =  res.cashier
        
        _logger.info(f'NAME CASHIER >>> { cashier_name }')
        
        res.update({
            'cashier_name': res.cashier
        })

        return res