from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PosPaymentUpdate(models.Model):
    _inherit = "pos.payment"
    
    credit_card_info_id = fields.Many2one('credit.card.info', string="Número de Tarjeta")
    
    @api.model
    def update_invoice_payments_widget(self, statementFlated, results):
        _logger.info("Inicio de update_invoice_payments_widget")
        
        for result in results:
            pos_order_id = result['id']
            pos_payments = self.search([('pos_order_id', '=', pos_order_id)])
            
            # Filtrar pagos con 'apply_card' en True
            pos_payments_filtered = pos_payments.filtered(lambda payment: payment.payment_method_id.apply_card)
            
            for statement in statementFlated:
                creditCard = statement.get("creditCard")
                credit_card = self.env['credit.card'].search([('name', '=', creditCard.get('card'))], limit=1)
                
                credit_card_info = self.env['credit.card.info'].create({
                    'credit_card_id': credit_card.id,
                    'recap': creditCard.get('recap'),
                    'authorization': creditCard.get('auth'),
                    'reference': creditCard.get('ref'),
                })             
                
                for pos_payment in pos_payments_filtered:
                    if pos_payment.amount == statement.get('amount') and not credit_card_info.pos_payment_id and not pos_payment.credit_card_info_id:
                        _logger.info(f"Asociando credit_card_info {credit_card_info.id} a pos_payment {pos_payment.id}")
                        
                        credit_card_info.write({'pos_payment_id': pos_payment.id})
                        pos_payment.write({'credit_card_info_id': credit_card_info.id})


                        