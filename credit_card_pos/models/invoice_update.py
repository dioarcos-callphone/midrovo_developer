from odoo import models, api

class InvoiceUpdate(models.Model):
    _inherit = "pos.order"
    
    @api.model
    def update_invoice_payments_widget(self, credit_card, results):
        for result in results:
            account_move = result['account_move']
            invoice = self.env['account.move'].search([('id', '=', account_move)])
            
            if invoice:
                invoice_payment_widget = invoice.invoice_payments_widget
                invoice_payment_widget['credit_card'] = credit_card                
                invoice.write({ 'invoice_payments_widget': invoice_payment_widget })