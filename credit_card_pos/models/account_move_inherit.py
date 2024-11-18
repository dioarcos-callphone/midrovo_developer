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
                        # Agregar más campos personalizados al diccionario reconciled_vals
                        _logger.info(payment)
                        _logger.info(f'OBTENIENDO PAYMENTS IDS >>> { move.pos_order_ids.payment_ids }')