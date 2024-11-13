from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class InvoiceUpdate(models.Model):
    _inherit = "pos.payment"
    
    credit_card_info_ids = fields.One2many('credit.card.info', 'pos_payment_id', string="Tarjetas de Crédito")
    
    @api.model
    def update_invoice_payments_widget(self, credit_cards, results):
        for result in results:
            pos_order_id = result['id']
            pos_payment = self.search([('pos_order_id', '=', pos_order_id)])
            
            if pos_payment:
                if pos_payment.payment_method_id:
                    payment_methods = pos_payment.payment_method_id
                    for payment_method in payment_methods:
                        if payment_method.apply_card:                        
                            for card in credit_cards:
                                credit_card = self.env['credit.card'].search([('name', '=', card.get('card'))], limit=1)
                                self.env['credit.card.info'].create({
                                    'pos_payment_id': pos_payment.id,
                                    'credit_card_id': credit_card.id,
                                    'recap': card.get('recap'),
                                    'authorization': card.get('auth'),
                                    'reference': card.get('ref'),
                                })

               