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
            _logger.info(f'MOSTRANDO MOVE >>> { move.invoice_payments_widget }')
            # if move.state == 'posted' and move.is_invoice(include_receipts=True):
            #     # Personaliza o añade campos adicionales a payments_widget_vals
            #     if move.invoice_payments_widget:
            #         for payment in move.invoice_payments_widget.get('content', []):
            #             payment['custom_field'] = 'Valor personalizado'  # Ejemplo