from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PosPaymentUpdate(models.Model):
    _inherit = "pos.payment"
    
    credit_card_info_id = fields.Many2one('credit.card.info', string="Número de Tarjeta")
    
    @api.model
    def update_invoice_payments_widget(self, statementFlated, results):
        for result in results:
            pos_order_id = result['id']
            pos_payments = self.search([('pos_order_id', '=', pos_order_id)])
            
            # Filtrar los pagos con 'apply_card' en True
            card_payments = pos_payments.filtered(lambda payment: payment.payment_method_id.apply_card)
            
            # Crear un mapa de pagos por montos y métodos de pago
            payment_map = {}
            for payment in card_payments:
                key = (payment.amount, payment.payment_method_id.id)
                payment_map.setdefault(key, []).append(payment)
            
            # Procesar cada entrada de statementFlated
            for statement in statementFlated:
                creditCard = statement.get("creditCard")
                if not creditCard:
                    continue
                
                # Buscar o crear la tarjeta de crédito
                credit_card = self.env['credit.card'].search([('name', '=', creditCard.get('name'))], limit=1)
                if not credit_card:
                    _logger.warning(f"Tarjeta de crédito no encontrada: {creditCard.get('name')}")
                    continue
                
                # Clave de coincidencia
                key = (statement.get('amount'), statement.get('payment_method_id'))
                if key in payment_map:
                    # Obtener el siguiente pago disponible para la clave
                    payment = payment_map[key].pop(0)
                    
                    # Verificar si ya existe una relación
                    existing_info = self.env['credit.card.info'].search([
                        ('recap', '=', creditCard.get('recap')),
                        ('authorization', '=', creditCard.get('auth')),
                        ('reference', '=', creditCard.get('reference')),
                        ('pos_payment_id', '=', payment.id),
                    ], limit=1)
                    
                    if not existing_info:
                        # Crear nueva relación
                        credit_card_info = self.env['credit.card.info'].create({
                            'credit_card_id': credit_card.id,
                            'recap': creditCard.get('recap'),
                            'authorization': creditCard.get('auth'),
                            'reference': creditCard.get('reference'),
                            'pos_payment_id': payment.id,
                        })
                        payment.write({'credit_card_info_id': credit_card_info.id})
                    
                    # Si no hay más pagos para esta clave, eliminar del mapa
                    if not payment_map[key]:
                        del payment_map[key]
