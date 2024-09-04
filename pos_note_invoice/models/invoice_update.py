from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def note_update_invoice(self, nota, results):
        for result in results:
            account_move = result['account_move']
            invoice = self.env['account.move'].search([('id', '=', account_move)])
            
            if invoice:
                invoice.write({ 'narration': nota })
                
                return invoice
            
        return None
    