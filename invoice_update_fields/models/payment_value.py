from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago(self):
        pass
    
    @api.model
    def _l10n_ec_get_payment_data(self):        
        # result = self.env['account.move.sri.lines'].search([], order='id desc', limit=1)
        
        # pay_term_line_ids = self.line_ids.filtered(
        #     lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        # )
        
        # for line in pay_term_line_ids:
        #     _logger.info(f'OBTENIENDO POS REFERENCE >>> { line.move_id.ref }')
        #     pos_id = self.env['pos.order'].search([('pos_reference', '=', line.move_id.ref)])
        #     _logger.info(f'OBTENIENDO ID DE POS ORDER >>> { pos_id }')
        #     # pos_id.get_invoice_field(pos_id.id)
            
        result = self.l10n_ec_sri_payment_ids.filtered(
            lambda line: line.payment_valor > 0
        )
        
        _logger.info(f'MOSTRANDO RESULTADO SRI LINES >>> { result }')      

        return super(PaymentValue, self)._l10n_ec_get_payment_data()

class PosOrder(models.Model):
    _inherit = 'pos.order'

    sale_barcode = fields.Char()

    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])

        return {
            'invoice_id': invoice_id.id,
            'invoice_name': invoice_id.name,
            'invoice_number': invoice_id.l10n_latam_document_number,
            'xml_key': invoice_id.l10n_ec_authorization_number,
        }
        
    def _l10n_ec_get_payment_data(self, pos_reference):
        payment_data = []
        pos_id = self.search([('pos_reference', '=', pos_reference)])
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])
        
        
        result = self.env['account.move.sri.lines'].search([('move_id','=',invoice_id.id)])
        
        for line in result:
            payment_vals = {
                'payment_code': line.l10n_ec_sri_payment_id.code,
                'payment_total': line.payment_valor,
                'payment_name':line.l10n_ec_sri_payment_id.name,
            }
            
            payment_data.append(payment_vals)
            
        return payment_data
            
        
        
        
        
