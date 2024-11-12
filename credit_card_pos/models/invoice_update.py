from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class InvoiceUpdate(models.Model):
    _inherit = "account.move"
    
    credit_card_info_ids = fields.One2many(
        'credit.card.info',
        'account_move_id',
        string="Tarjetas de Crédito"
    )
    
    @api.model
    def update_invoice_payments_widget(self, credit_cards, results):
        for result in results:
            account_move = result['account_move']
            invoice = self.search([('id', '=', account_move)])
            
            if invoice:
                for card in credit_cards:
                    credit_card = self.env['credit.card'].search([('name', '=', card.get('card'))], limit=1)
                    self.env['credit.card.info'].create({
                        'account_move_id': invoice.id,
                        'credit_card_id': credit_card.id,
                        'recap': card.get('recap'),
                        'authorization': card.get('auth'),
                        'reference': card.get('ref'),
                    })

                