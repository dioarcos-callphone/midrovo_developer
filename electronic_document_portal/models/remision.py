from odoo import models, fields
from odoo.tools import (get_lang)

class Remission(models.Model):
    _inherit = 'account.remision'

    state_sri = fields.Selection([
        ('draft', u'Creado'),
        ('signed', u'Firmado'),
        ('waiting', u'En Espera de Autorización'),
        ('authorized', u'Autorizado'),
        ('returned', u'Devuelta'),
        ('rejected', u'No Autorizado'),
        ('cancel', u'Cancelado')
    ], string=u'Estado', readonly=True, related='xml_data_id.state')
    
    # EXTENDS portal portal.mixin
    def _compute_access_url(self):
        super()._compute_access_url()
        for remision in self:
            remision.access_url = '/my/remissions/%s' % (remision.id)
      
    # Genera el nombre del archivo PDF del reporte  
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Guia de remision-%s' % (self.l10n_latam_document_number)
    
    def _get_mail_template(self):
        return 'ec_account_edi.ec_email_template_edi_invoice'

    

    def action_remission_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('electronic_document_portal.email_template_remission', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.remision',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="electronic_document_portal.mail_template_data_notification_email_account_remision",
            force_email=True
        )
        return {
            'name': _('Componer Correo'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
    

class RemissionLine(models.Model):
    _inherit = 'account.remision.line'