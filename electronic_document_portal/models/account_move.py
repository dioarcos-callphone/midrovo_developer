from odoo import _, api, fields, models
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    sri_message_ids = fields.One2many(
        related='xml_data_id.message_ids',
        string="Message Lines"
    )

    view_xml_data = fields.One2many(
        related='xml_data_id',
        string='Xml Data Form'
    )

    def _get_mail_template(self):
        if self.move_type in ['out_invoice', 'in_invoice', 'out_refund']:
            return 'ec_account_edi.ec_email_template_edi_invoice'
        return ('account.email_template_edi_credit_note' if all(
            move.move_type == 'out_refund' for move in self) else 'account.email_template_edi_invoice')
    
    def unlink(self):
        if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_nodelete"):
            raise UserError("No consta con permisos para eliminar éste documento porfavor comuníquese con el departamento de sistemas.")
        
        if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_posted"):
            self.state = 'draft'

        return super(AccountMove, self).unlink()

    