from odoo import models, fields, api

class InvoiceUpdate(models.Model):
    _inherit = "account.move"
    
    # Campo JSON para almacenar los detalles de la tarjeta de crédito
    credit_card_info = fields.Json(string="Informacion de Tarjeta de Crédito")
    
    @api.model
    def update_invoice_payments_widget(self, credit_card, results):
        for result in results:
            account_move = result['account_move']
            invoice = self.search([('id', '=', account_move)])
            
            if invoice:              
                invoice.write({ 'credit_card_info': credit_card })
                