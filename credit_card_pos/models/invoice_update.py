from odoo import models, api

import logging
_logger = logging.getLogger(__name__)


class InvoiceUpdate(models.Model):
    _inherit = "pos.order"
    
    @api.model
    def update_invoice_payments_widget(self, credit_card, results):
        for result in results:
            account_move = result['account_move']
            invoice = self.env['account.move'].search([('id', '=', account_move)])
            _logger.info(f'MOSTRANDO FACTURA >>> { invoice.invoice_payments_widget }')
            # if invoice:
            #     invoice.write({ 'narration': nota })