from odoo import models, fields, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools import (get_lang)

class Remission(models.Model):
    _inherit = 'account.remision'

    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'account.remision')], string='Attachments')

    is_remission_sent = fields.Boolean(
        readonly=True,
        default=False,
        copy=False,
        tracking=True,
    )

    state_sri = fields.Selection([
        ('draft', u'Creado'),
        ('signed', u'Firmado'),
        ('waiting', u'En Espera de Autorización'),
        ('authorized', u'Autorizado'),
        ('returned', u'Devuelta'),
        ('rejected', u'No Autorizado'),
        ('cancel', u'Cancelado')
    ], string=u'Estado', readonly=True, related='xml_data_id.state')

    xml_authorized = fields.Binary(string=u"Archivo XML Autorizado", related='xml_data_id.xml_authorized', copy=False)
    xml_name = fields.Char(string=u"Archivo XML", related='xml_data_id.xml_name')

    remission_send_ids = fields.Many2many('account.remission.send', 'account_remission_account_remission_send_rel')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.uid)

    sri_message_ids = fields.One2many(
        related='xml_data_id.message_ids',
        string="Message Lines"
    )

    # EXTENDS portal portal.mixin
    def _compute_access_url(self):
        super()._compute_access_url()
        for remision in self:
            remision.access_url = '/my/remissions/%s' % (remision.id)

    def send_sri(self):
        self.xml_data_id.send_file()
      
    # Genera el nombre del archivo PDF del reporte  
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Guia de remision-%s' % (self.l10n_latam_document_number)
    
    def _get_mail_template(self):
        return 'electronic_document_portal.ec_email_template_edi_remission'
    
    def action_remission_print(self):
        return self.env.ref('ec_account_edi.e_delivery_note_qweb').report_action(self)


    def action_remission_sent(self):
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
        compose_form = self.env.ref('electronic_document_portal.account_remission_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.remision',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.remision',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_remission_as_sent=True,
            default_email_layout_xmlid="mail.mail_notification_layout_with_responsible_signature",
            model_description="",
            force_email=True,
            active_ids=self.ids,
        )

        report_action = {
            'name': _('Send Remission'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.remission.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

        if self.env.is_admin() and not self.env.company.external_report_layout_id and not self.env.context.get('discard_logo_check'):
            return self.env['ir.actions.report']._action_configure_external_report_layout(report_action)

        return report_action
    
    # def unlink(self):
    #     if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_nodelete"):
    #         raise UserError("No consta con permisos para eliminar éste documento porfavor comuníquese con el departamento de sistemas.")
        
    #     return super().unlink()
    
    def unlink(self):
        if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_nodelete"):
            raise UserError("No consta con permisos para eliminar éste documento porfavor comuníquese con el departamento de sistemas.")
        
        if self.env.user.has_group("electronic_document_portal.portal_user_internal_group_posted"):
            self.state = 'draft'   

        xml_model = self.env['sri.xml.data']
        #si esta en modo produccion, no permitir eliminar el documento
        if xml_model.is_enviroment_production(self.document_type):
            for remision in self:
                if remision.state != 'draft':
                    raise ValidationError(_(u"¡No es posible desvincular la nota de entrega en el entorno de producción!"))
        return super(Remission, self).unlink()

class RemissionLine(models.Model):
    _inherit = 'account.remision.line'