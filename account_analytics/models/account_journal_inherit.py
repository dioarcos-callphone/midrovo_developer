from odoo import models, fields, api

class AccountJournalInherit(models.AbstractModel):
    _inherit = 'account.journal'
    _description = 'Modulo que establece la relacion con cuentas analíticas'
    
    analytic_id = fields.Many2one(
        string='Cuenta Analítica',
        comodel_name='account.analytic.account'
    )