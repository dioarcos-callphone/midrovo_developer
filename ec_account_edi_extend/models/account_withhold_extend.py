from odoo import models, field, api

class AccountWithholdExtend(models.Model):
    _inherit = ['account.withhold', 'portal.mixin']
    
    