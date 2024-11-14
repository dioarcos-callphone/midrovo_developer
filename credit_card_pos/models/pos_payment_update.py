from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class PosPaymentUpdate(models.Model):
    _inherit = "pos.payment"
    
    credit_card_info_ids = fields.One2many('credit.card.info', 'pos_payment_id', string="Tarjetas de Crédito")
    
    @api.model
    def update_invoice_payments_widget(self, statementFlated, results):
        _logger.info(f'MOSTRANDO STATEMENT >>>> { statementFlated }')
        
        for result in results:
            pos_order_id = result['id']
            pos_payments = self.search([('pos_order_id', '=', pos_order_id)])
            
            # Filtrar los pagos cuyo método de pago tiene 'apply_card' en True
            card_payments = pos_payments.filtered(lambda payment: payment.payment_method_id.apply_card)
            
            # if card_payments:
            #     for payment in card_payments:      
            #         for card in credit_cards:
            #             credit_card = self.env['credit.card'].search([('name', '=', card.get('card'))], limit=1)
            #             self.env['credit.card.info'].create({
            #                 'pos_payment_id': payment.id,
            #                 'credit_card_id': credit_card.id,
            #                 'recap': card.get('recap'),
            #                 'authorization': card.get('auth'),
            #                 'reference': card.get('ref'),
            #             })

               