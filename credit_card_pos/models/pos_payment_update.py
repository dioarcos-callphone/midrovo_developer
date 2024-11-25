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
            
            _logger.info(pos_payments_filtered)
            
            for statement in statementFlated:
                _logger.info(statement)