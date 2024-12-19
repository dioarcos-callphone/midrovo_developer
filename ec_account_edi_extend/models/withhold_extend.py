from odoo import models

class WithholdExtend(models.Model):
    _inherit = 'account.withhold'
    
    # EXTENDS portal portal.mixin
    def _compute_access_url(self):
        super()._compute_access_url()
        for withhold in self:
            withhold.access_url = '/my/withholdings/%s' % (withhold.id)