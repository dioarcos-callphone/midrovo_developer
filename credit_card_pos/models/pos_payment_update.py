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
            _logger.info(f"Pagos encontrados para la orden {pos_order_id}: {pos_payments.ids}")
            
            # Filtrar pagos con 'apply_card' en True
            card_payments = pos_payments.filtered(lambda payment: payment.payment_method_id.apply_card)
            
            for statement in statementFlated:
                creditCard = statement.get("creditCard")
                if not creditCard:
                    _logger.warning("statementFlated contiene una entrada sin 'creditCard'")
                    continue
                
                # Buscar o crear la tarjeta de crédito
                credit_card = self.env['credit.card'].search([('name', '=', creditCard.get('name'))], limit=1)
                if not credit_card:
                    _logger.warning(f"Tarjeta de crédito no encontrada: {creditCard.get('name')}")
                    continue
                
                for payment in card_payments:
                    # Validar condiciones antes de crear
                    if (statement.get('amount') == payment.amount and 
                        statement.get('payment_method_id') == payment.payment_method_id.id and
                        not payment.credit_card_info_id):
                        
                        _logger.info(f"Creando credit.card.info para payment_id {payment.id}")
                        
                        # Crear registro en credit.card.info
                        try:
                            credit_card_info = self.env['credit.card.info'].create({
                                'credit_card_id': credit_card.id,
                                'recap': creditCard.get('recap'),
                                'authorization': creditCard.get('auth'),
                                'reference': creditCard.get('reference'),
                                'pos_payment_id': payment.id,
                            })
                            payment.write({'credit_card_info_id': credit_card_info.id})
                        except Exception as e:
                            _logger.error(f"Error creando credit.card.info: {str(e)}")
