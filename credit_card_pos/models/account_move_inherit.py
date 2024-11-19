from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    @api.depends('move_type', 'line_ids.amount_residual')
    def _compute_payments_widget_reconciled_info(self):
        # Llamar al método original si quieres conservar la lógica
        super(AccountMoveInherit, self)._compute_payments_widget_reconciled_info()
        
        # Agregar lógica personalizada
        for move in self:
            
            if move.state == 'posted' and move.is_invoice(include_receipts=True):
                # Verificar si ya hay contenido en el widget
                if move.invoice_payments_widget and move.invoice_payments_widget.get('content'):
                    
                    for payment in move.invoice_payments_widget['content']:
                        _logger.info(f'MOSTRANDO CONTENT >>> { payment }')
                        
                        pos_order = move.pos_order_ids
                        
                        if pos_order:
                            for p in pos_order.payment_ids:
                                # _logger.info(f'MOVE { move.id } - { payment.credit_card_info_id }')
                                
                                if p.credit_card_info_id:
                                    payment['credit_card'] = p.credit_card_info_id.credit_card_id.name
                                    payment['recap'] = p.credit_card_info_id.recap
                                    payment['auth'] = p.credit_card_info_id.authorization
                                    payment['ref'] = p.credit_card_info_id.reference
                        
                        
                        _logger.info(f'MOSTRANDO CONTENT >>> { payment }')