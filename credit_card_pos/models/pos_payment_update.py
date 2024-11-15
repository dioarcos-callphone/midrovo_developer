from odoo import models, fields, api

class PosPaymentUpdate(models.Model):
    _inherit = "pos.payment"
    
    credit_card_info_ids = fields.One2many('credit.card.info', 'pos_payment_id', string="Tarjetas de Crédito")
    
    @api.model
    def update_invoice_payments_widget(self, statementFlated, results):       
        for result in results:
            pos_order_id = result['id']
            pos_payments = self.search([('pos_order_id', '=', pos_order_id)])
            
            # Filtrar los pagos cuyo método de pago tiene 'apply_card' en True
            card_payments = pos_payments.filtered(lambda payment: payment.payment_method_id.apply_card)               
            
            if card_payments:
                for statement in statementFlated:
                    creditCard = statement.get('creditCard')
                    for payment in card_payments:      
                        credit_card = self.env['credit.card'].search([('name', '=', creditCard.get('card'))], limit=1)
                        
                        if statement.get('amount') == payment.amount and statement.get('payment_method_id') == payment.payment_method_id.id:
                            self.env['credit.card.info'].create({
                                'pos_payment_id': payment.id,
                                'credit_card_id': credit_card.id,
                                'recap': creditCard.get('recap'),
                                'authorization': creditCard.get('auth'),
                                'reference': creditCard.get('ref'),
                            })
                                                   