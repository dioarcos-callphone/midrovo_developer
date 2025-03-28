from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_mail_template(self):
        if self.move_type in ['out_invoice', 'in_invoice', 'out_refund']:
            return 'ec_account_edi.ec_email_template_edi_invoice'
        return ('account.email_template_edi_credit_note' if all(
            move.move_type == 'out_refund' for move in self) else 'account.email_template_edi_invoice')
    