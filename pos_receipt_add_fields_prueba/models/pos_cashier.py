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
        
        _logger.info('INVOICES >>> %s' % invoice_id.partner_id)
        
        res = super(PosCashier, self).get_invoice_field(id)

        cashier_name = pos_id.user_id.name if pos_id.user_id else 'Desconocido'
        
        _logger.info(f'NAME CASHIER >>> {cashier_name}')
        
        res.update({
            'cashier_name': cashier_name,
        })

        return res