from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

# class PaymentValue(models.Model):
#     _inherit = 'account.move'
    
#     @api.model
#     def _get_default_forma_pago_sri(self):
#         pass
    
#     l10n_ec_sri_payment_id = fields.Many2one(
#         comodel_name="l10n_ec.sri.payment",
#         string="Payment Method (SRI)",
#     )
    
#     @api.model
#     def _l10n_ec_get_payment_data(self):
#         payment_data = []
        
#         account_move_line = self.line_ids.filtered(
#             lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
#         )
        
#         move_id = account_move_line.move_id.id
        
#         _logger.info(f'CODIGO DE MOVE LINE >>> { move_id }')
        
#         account_move_sri_lines = self.env['account.move.sri.lines'].sudo().search([('move_id','=',move_id)])
        
#         #id = account_move_sri_lines.id
                
#         #_logger.info(f'VALORES DEL SRI LINES >>> { id }')
        
#         _logger.info(f'ACCOUNT MOVE LINE 0 >>> { account_move_line }')
#         _logger.info(f'ACCOUNT MOVE SRI LINES 1 >>> { account_move_sri_lines }')
                
#         for line in account_move_line:
#             payment_vals = {
#                 'payment_code': 16,
#                 'payment_total': 200,
#                 'payment_name': 'Debito',
#             }
        
#             payment_data.append(payment_vals)
        
#         _logger.info(f'MOSTRANDO EL PAYMENT DATA 1 >>> { payment_data }')

#         return payment_data
    
# # class InheritAccountMoveSriLines(models.Model):
# #     _inherit = 'account.move.sri.lines'

# #     def _get_default_forma_pago(self):
# #         return self.env['l10n_ec.sri.payment'].search([('code', '=', '16')])
    

# #     l10n_ec_sri_payment_id = fields.Many2one(
# #         comodel_name="l10n_ec.sri.payment",
# #         string="Payment Method (SRI)",
# #         required=True, 
# #         ondelete='cascade', 
# #         index=True
# #     )
    
# #     #parameter to One2many, 
# #     move_id = fields.Many2one(  "account.move", 
# #                                 string="Account_key",
# #                                 required=True,
# #                                 readonly=True,
# #                                 index=True,
# #                                 auto_join=True,
# #                                 ondelete="cascade",
# #                                 check_company=True,
# #                             )
    
# #     payment_valor = fields.Float( string="Price value",
# #                                     compute='_compute_payment_valor', store=True, readonly=False, precompute=True,
# #                                     digits='Payment value',)
    
# #     @api.model
# #     @api.depends("payment_valor","move_id")
# #     def _compute_payment_valor(self):
# #         value = 0.00
# #         for line in self:
# #             if ( line.move_id[0]):
# #                 invoices = self.env["account.move"].browse([line.move_id[0].id])
# #                 _logger.info(f'MOSTRANDO INVOICES >>> { invoices }')
# #                 value = invoices._get_default_payment_valor()
# #                 line.payment_valor = value


class AccountMoveCompensa(models.Model):
    _inherit = "account.move"
    
    # Heredamos el campo 'compensa'
    compensa = fields.Float(string='Compensación')

    # Heredamos el método '_l10n_ec_get_payment_data' para modificar su funcionalidad
    def _l10n_ec_get_payment_data(self):
        """ Get payment data for the XML.  """
        payment_data = super(AccountMoveCompensa, self)._l10n_ec_get_payment_data()

        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )

        for line in pay_term_line_ids:
            payment_vals = {
                'payment_code': self.l10n_ec_sri_payment_id.code,
                'payment_total': 200,
                'payment_name': 'deposito',
            }
            if self.invoice_payment_term_id and line.date_maturity:
                payment_vals.update({
                    'payment_term': max(((line.date_maturity - self.invoice_date).days), 0),
                    'time_unit': "días",
                })
            payment_data.append(payment_vals)

        # Añadimos la lógica personalizada para la compensación
        if self.compensa > 0:
            payment_vals = {
                'payment_code': '15',
                'payment_total': self.compensa,
                'payment_name': 'Compensación de Deudas',
            }
            payment_vals.update({
                'payment_term': 1,
                'time_unit': "días",
            })
            payment_data.append(payment_vals)

        return payment_data