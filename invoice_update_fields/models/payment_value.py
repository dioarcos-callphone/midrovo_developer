from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

sri_lines = []

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):
        try:
            _logger.info('ENTRA AQUIIIIIIIIIII')
            _logger.info(f'INVOICE NAME >>> { invoice_name }')
            _logger.info(f'SRI LINES >>> { sri_lines }')
            # Buscar la factura por referencia
            invoice = self.env['account.move'].search([('ref', '=', invoice_name)], limit=1)
            
            _logger.info(invoice)
            
            if invoice:
                for line in sri_lines:
                    sri_payment = self.env['l10n_ec.sri.payment'].search([('id', '=', line['l10n_ec_sri_payment_id'])])
                    sri_lines_new = self.env['account.move.sri.lines'].create({
                        'l10n_ec_sri_payment_id': sri_payment.id,
                        'move_id': invoice.id,
                        'payment_valor': line['payment_valor']
                    })
                    
                    _logger.info(f'REGISTRO CREADO >>> {sri_lines_new}')
                
                # Agregar las líneas SRI
                # invoice.write({'l10n_ec_sri_payment_ids': [(0, 0, line) for line in sri_lines]})
                
                _logger.info(f'MOSTRANDO ACTUALIZACION >>> { invoice.l10n_ec_sri_payment_ids }')

        except Exception as e:
            # Capturar y registrar errores
            _logger.error("Ocurrió un error en update_account_move_sri_lines: %s", str(e))
            return False


    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_contable = super(PaymentValue, self)._l10n_ec_get_payment_data()
        payment_data = []
        
        if self:
            _logger.info(f'MOSTRANDO SELF { self }')
            
            query = """
                SELECT l.id, l.move_id, s.code, s.name, l.payment_valor
                FROM account_move_sri_lines l INNER JOIN l10n_ec_sri_payment s
                ON l.l10n_ec_sri_payment_id = s.id
                WHERE move_id = %s
            """
            # Ejecutar la consulta SQL con el parámetro 'move_id'
            self.env.cr.execute(query, (self.id,))
            results = self.env.cr.fetchall()  # Obtiene los resultados de la consulta
            
            _logger.info(f'MOSTRANDO RESULT >>>> { results }')
                
            sri_lines = self.env['account.move.sri.lines'].sudo().search([('move_id','=', self.id)])
            
            _logger.info(f'MOSTRANDO SRI LINEESSS >>> { sri_lines }')
            
            sri_payments = self.l10n_ec_sri_payment_ids
            if sri_payments:
                for sri_payment in sri_payments:
                    _logger.info(f'MOSTRANDO SRI PAYMENT { sri_payment }')
                    _logger.info(f'MOSTRANDO L10N SRI PAYMENT ID { sri_payment.l10n_ec_sri_payment_id }')
                    payment_values = {
                        'payment_code': sri_payment.l10n_ec_sri_payment_id.code,
                        'payment_total': sri_payment.payment_valor,
                        'payment_name': sri_payment.l10n_ec_sri_payment_id.name
                    }
            
                    payment_data.append(payment_values)
                    
        # _logger.info('NO ENTRA')            
        
          
        # if sri_lines:
        #     for sri_line in sri_lines:
        #         l10n_ec_sri_payment = self.env['l10n_ec.sri.payment'].search([('id','=', sri_line.l10n_ec_sri_payment_id)])
                
        #         if l10n_ec_sri_payment:
        #             payment_values = {
        #                 'payment_code': l10n_ec_sri_payment.code,
        #                 'payment_total': sri_line.payment_valor,
        #                 'payment_name': l10n_ec_sri_payment.name
        #             }
            
        #             payment_data.append(payment_values)
        
        return payment_data if payment_data else payment_contable
