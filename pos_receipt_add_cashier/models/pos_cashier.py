from odoo import models, fields, api
import logging 

_logger = logging.getLogger(__name__)

class PosCashier(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])
        
        cashier_name = pos_id.cashier
        invoice_id.invoice_user_id.name = cashier_name
        #invoice_id.write({'invoice_user_id': cashier_name})
        
        res = super(PosCashier, self).get_invoice_field(id)
        
        cashier_account = invoice_id.invoice_user_id
        
        _logger.info(f'NAME CASHIER >>> {cashier_name}')
        _logger.info(f'NAME CASHIER DEL ACCOUNT MOVE >>> {cashier_account}')
        
        res.update({
            'cashier_name': cashier_name,
        })

        return res