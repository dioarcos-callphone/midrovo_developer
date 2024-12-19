from odoo import models, api, fields

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
    
    # Agregar el campo de partner commercial (similar al de account.move)
    commercial_partner_id = fields.Many2one(
        'res.partner',
        string='Commercial Entity',
        compute='_compute_commercial_partner_id',
        store=True, readonly=True,
        ondelete='restrict',
    )

    @api.depends('partner_id')
    def _compute_commercial_partner_id(self):
        for record in self:
            if record.partner_id:
                record.commercial_partner_id = record.partner_id.commercial_partner_id
            else:
                record.commercial_partner_id = False
                
    
class WithholdLineExtend(models.Model):
    _inherit = 'account.withhold.line'