from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

data = []
query = 'SELECT code, name FROM l10n_ec_sri_payment WHERE id = %s'

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago(self):
        pass
    
    l10n_ec_sri_payment_ids = fields.One2many('account.move.sri.lines', 'move_id', required = True)
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):        
        try:
            for line in sri_lines:
                data.append(line)
            
            # Agrega las sri_lines al acount_move
            lines_value = []
            invoice_id = self.env['account.move'].search(
            [('ref', '=', invoice_name)])
            invoice = self.env['account.move'].browse(invoice_id.id)
            if invoice :
                for sri_line in sri_lines:
                    invoice.write({'l10n_ec_sri_payment_ids': [(0, 0, sri_line)]})
                    lines_value.append( (0, 0, sri_line))
                invoice.env.cr.commit()
        except Exception as e:
            # Captura la excepción y registra el error
            _logger.error("Ocurrió un error: %s", str(e))
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        cr = self.env.cr
        payment_data = []
        _logger.info(f'SE OBTIENE LOS SRI LINES >>> { data }')
        
        for line in data:
            payment_id = line['l10n_ec_sri_payment_id']
            _logger.info(f'ID DEL PAYMENT SRI >>> { payment_id }')
            cr.execute(query,(payment_id,))
            result = cr.fetchall()
            #l10n_ec_sri_payment = self.env['l10n_ec_sri_payment'].search([('id', '=', payment_id)])
            
            _logger.info(f'OBTENIENDO EL RESULT >>> { result }')
            payment_values = {
                'payment_code': 'l10n_ec_sri_payment.code',
                'payment_total': line.payment_valor,
                'payment_name': 'l10n_ec_sri_payment.name',
            }
            
            payment_data.append(payment_values)
        
        _logger.info(f'SE OBTIENE EL PAYMENT DATA >>> { payment_data }')  
        
        # move_id = pay_term_line_ids.move_id.id
        
        # result = self.env['account.move.sri.lines'].search([('move_id','=', move_id)], limit=1)
        
        # result = await self.async_search(move_id)
        
        # _logger.info(f'OBTENIENDO SRI LINES >>> { result }')
        # _logger.info(f'OBTENIENDO MOVE LINE >>> { pay_term_line_ids }')
        
        data.clear() 

        return payment_data
        #return super(PaymentValue, self)._l10n_ec_get_payment_data()
    


# class PosOrder(models.Model):
#     _inherit = 'pos.order'

#     sale_barcode = fields.Char()

#     @api.model
#     def get_invoice_field(self, id):
#         payment_data = []
#         pos_id = self.search([('pos_reference', '=', id)])
#         invoice_id = self.env['account.move'].search(
#             [('ref', '=', pos_id.name)])
        
#         result = self.env['account.move.sri.lines'].search([('move_id','=',invoice_id.id)])
#         _logger.info(f'OBTENIENDO RESULT >>> { result }')
        
#         for line in result:
#             payment_vals = {
#                 'payment_code': line.l10n_ec_sri_payment_id.code,
#                 'payment_total': line.payment_valor,
#                 'payment_name':line.l10n_ec_sri_payment_id.name,
#             }
            
#             self.env['account.move.sri.lines'].write({
#                 'l10n_ec_sri_payment_id': line.l10n_ec_sri_payment_id.code,
#                 'payment_valor': line.payment_valor,
#             })
            
#             payment_data.append(payment_vals)

#         return {
#             'invoice_id': invoice_id.id,
#             'invoice_name': invoice_id.name,
#             'invoice_number': invoice_id.l10n_latam_document_number,
#             'xml_key': invoice_id.l10n_ec_authorization_number,
#             'payment_data': payment_data
#         }
        
    # def _l10n_ec_get_payment_data(self, pos_reference):
    #     payment =  self.get_invoice_field(pos_reference.pos_reference)
    #     payment_data = []
    #     pos_id = self.search([('pos_reference', '=', pos_reference.pos_reference)])
    #     invoice_id = self.env['account.move'].search(
    #         [('ref', '=', pos_id.name)])
        
    #     payment = payment['payment_data']
    #     _logger.info(f'OBTENIENDO DEL INVOICE >>> { payment }')        
        
    #     result = self.env['account.move.sri.lines'].search([('move_id','=',invoice_id.id)])
        
    #     _logger.info(f'OBTENIENDO RESULT >>> { result }')
        
    #     for line in result:
    #         payment_vals = {
    #             'payment_code': line.l10n_ec_sri_payment_id.code,
    #             'payment_total': line.payment_valor,
    #             'payment_name':line.l10n_ec_sri_payment_id.name,
    #         }
            
    #         payment_data.append(payment_vals)
            
    #     return payment_data
            
        
        
        
        
