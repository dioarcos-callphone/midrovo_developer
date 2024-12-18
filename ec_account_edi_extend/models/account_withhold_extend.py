from odoo import models

class AccountWithholdExtend(models.Model):
    _inherit = ['account.withhold', 'portal.mixin']
    
    