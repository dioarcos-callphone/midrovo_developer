from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools import (get_lang)

class Withhold(models.Model):
    _inherit = 'account.withhold'

    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'account.withhold')], string='Attachments')

    is_withhold_sent = fields.Boolean(
        readonly=True,
        default=False,
        copy=False,
        tracking=True,
    )

    withhold_send_ids = fields.Many2many('account.withhold.send', 'account_withhold_account_withhold_send_rel')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.uid)

    sri_message_ids = fields.One2many(
        related='xml_data_id.message_ids',
        string="Message Lines"
    )

    xml_authorized = fields.Binary(string=u"Archivo XML Autorizado", related='xml_data_id.xml_authorized', copy=False)
    
    # EXTENDS portal portal.mixin
    def _compute_access_url(self):
        super()._compute_access_url()
        for withhold in self:
            withhold.access_url = '/my/retentions/%s' % (withhold.id)
      
    # Genera el nombre del archivo PDF del reporte  
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Retencion-%s' % (self.l10n_latam_document_number)
    

    def _get_mail_template(self):
        return 'electronic_document_portal.ec_email_template_edi_retention'
    
    
    def action_withhold_print(self):
        return self.env.ref('ec_account_edi.e_retention_qweb').report_action(self)
    

    def action_withhold_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref(self._get_mail_template(), raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref('electronic_document_portal.account_withhold_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.withhold',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.withhold',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_withhold_as_sent=True,
            default_email_layout_xmlid="mail.mail_notification_layout_with_responsible_signature",
            model_description="",
            force_email=True,
            active_ids=self.ids,
        )

        report_action = {
            'name': _('Send Withhold'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.withhold.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

        if self.env.is_admin() and not self.env.company.external_report_layout_id and not self.env.context.get('discard_logo_check'):
            return self.env['ir.actions.report']._action_configure_external_report_layout(report_action)

        return report_action
    
    def unlink(self):
        if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_nodelete"):
            raise UserError("No consta con permisos para eliminar éste documento porfavor comuníquese con el departamento de sistemas.")
        
        return super().unlink()
    

    def unlink(self):
        for rec in self:
            if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_nodelete"):
                raise UserError("No consta con permisos para eliminar éste documento porfavor comuníquese con el departamento de sistemas.")

            if rec.state == 'posted':
                if rec.env.user.has_group("electronic_document_portal.portal_user_internal_group_posted"):
                    rec.state = 'draft'
                else:
                    raise UserError("No se permite borrar documentos que han sido publicados")

            # if rec.env.user.has_group("electronic_document_portal.portal_user_internal_group_nodelete"):
            #     raise UserError("No consta con permisos para eliminar este documento. Por favor comuníquese con el departamento de sistemas.")
        
        return super().unlink()

class WithholdLineExtend(models.Model):
    _inherit = 'account.withhold.line'
    