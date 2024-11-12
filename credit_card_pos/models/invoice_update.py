from odoo import models, api

import logging
_logger = logging.getLogger(__name__)


class InvoiceUpdate(models.Model):
    _inherit = "account.move"
    
    @api.model
    def update_invoice_payments_widget(self, credit_card, results):
        for result in results:
            account_move = result['account_move']
            invoice = self.search([('id', '=', account_move)])
            
            invoice_search = self.search([('id', '=', 2255)])
            
            _logger.info(f'MOSTRANDO PAYMENT WIDGTE DE FACTURA ANTERIOR >>> { invoice_search.invoice_payments_widget }')
            
            if invoice:
                invoice_payment_widget = invoice.invoice_payments_widget
                invoice_payment_widget['credit_card'] = credit_card                
                invoice.write({ 'invoice_payments_widget': invoice_payment_widget })
                