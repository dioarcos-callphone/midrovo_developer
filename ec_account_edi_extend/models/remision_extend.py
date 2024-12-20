from odoo import models

class RemisionExtend(models.Model):
    _inherit = 'account.remision'
    
    # EXTENDS portal portal.mixin
    def _compute_access_url(self):
        super()._compute_access_url()
        for remision in self:
            remision.access_url = '/my/shipping_guides/%s' % (remision.id)
      
    # Genera el nombre del archivo PDF del reporte  
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Guia de remision-%s' % (self.l10n_latam_document_number)
    
class RemisionLineExtend(models.Model):
    _inherit = 'account.remision.line'
    