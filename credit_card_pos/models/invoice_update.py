from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class InvoiceUpdate(models.Model):
    _inherit = "pos.payment"
    
    @api.model
    def update_invoice_payments_widget(self, credit_cards, results):
        for result in results:
            pos_order_id = result['id']
            pos_payment = self.search([('pos_order_id', '=', pos_order_id)])
            
            if pos_payment:
                _logger.info(f'POS PAYMENT >>> { pos_payment.pos_order_id }')
                # for card in credit_cards:
                #     credit_card = self.env['credit.card'].search([('name', '=', card.get('card'))], limit=1)
                #     self.env['credit.card.info'].create({
                #         'account_move_id': invoice.id,
                #         'credit_card_id': credit_card.id,
                #         'recap': card.get('recap'),
                #         'authorization': card.get('auth'),
                #         'reference': card.get('ref'),
                #     })

                