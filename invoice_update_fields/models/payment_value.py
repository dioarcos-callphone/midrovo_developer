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
        
        result = self.l10n_ec_sri_payment_ids.filtered(
            lambda line: line.payment_valor > 0
        )
        
        _logger.info(f'MOSTRANDO RESULTADO SRI LINES >>> { result }')      
        
        # for element in result:
        #     _logger.info(f'ACCOUNT MOVE ID >>> { element.move_id }')
        
        

        return super(PaymentValue, self)._l10n_ec_get_payment_data()

class PosOrder(models.Model):
    _inherit = 'pos.order'

    sale_barcode = fields.Char()

    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])
        
        
        result = self.env['account.move.sri.lines'].search([('mode_id','=',invoice_id.id)])
        
        _logger.info(f'OBTENIENDO EL SRI LINES >>> { result }')

        return {
            'invoice_id': invoice_id.id,
            'invoice_name': invoice_id.name,
            'invoice_number': invoice_id.l10n_latam_document_number,
            'xml_key': invoice_id.l10n_ec_authorization_number,
        }

