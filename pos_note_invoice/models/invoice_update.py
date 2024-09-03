from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    def get_note(self, note):
        return note
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        note_context = self.env.context.get('note_context')
        
        _logger.info(f'Nota recibida del contexto: {note_context}')
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        
        move_id = pay_term_line_ids.move_id.id
        
        account_move = self.search([('id', '=', move_id)])
        
        # account_move.write({ 'narration': 'ACTUALIZANDO NOTA' })
        
        _logger.info(f'OBTENIENDO EL PAY TERM >>> { pay_term_line_ids }')

        
        # _logger.info(f'SE OBTIENE EL PAYMENT DATA >>> { payment_data }')        
        # _logger.info(f'SE OBTIENE EL PAYMENT CONTABLE >>> { payment_contable }')
        
        return super(InvoiceUpdate, self)._l10n_ec_get_payment_data()