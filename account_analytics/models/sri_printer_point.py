from odoo import models, fields, api

class SriPrinterPointInherit(models.Model):
    _inherit = 'sri.printer.point'
    
    analytic_id = fields.Many2one(
        string='Cuenta Analítica',
        comodel_name='account.analytic.account'
    )