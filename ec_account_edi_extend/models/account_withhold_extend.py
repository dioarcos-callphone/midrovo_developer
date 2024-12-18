from odoo import models

class AccountWithholdExtend(models.Model):
    _inherit = 'account.withhold'
    
    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        return self.env['portal.mixin'].get_portal_url(self, suffix, report_type, download, query_string, anchor)
    
    