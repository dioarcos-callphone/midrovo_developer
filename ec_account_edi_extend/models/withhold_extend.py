from odoo import models

class WithholdExtend(models.Model):
    _inherit = 'account.withhold'
    
    # EXTENDS portal portal.mixin
    def _compute_access_url(self):
        super()._compute_access_url()
        for withhold in self:
            withhold.access_url = '/my/withholdings/%s' % (withhold.id)
      
    # Genera el nombre del archivo PDF del reporte  
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Retencion-%s' % (self.l10n_latam_document_number)