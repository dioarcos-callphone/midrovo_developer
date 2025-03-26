from odoo import models, fields

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
    
class RemisionLineExtend(models.Model):
    _inherit = 'account.remision.line'
    