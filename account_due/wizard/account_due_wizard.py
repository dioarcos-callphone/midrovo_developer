import io
import json
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class AccountDueWizard(models.TransientModel):
    _name = "account.due.wizard"
    _description = "Cuentas por Cobrar Vencidas"
    
    court_date = fields.Date(
        string = 'Fecha de corte',
        help = 'Fecha de corte para analizar el informe',
        required = True
    )
    
    client_id = fields.Many2one(
        string='Cliente',
        comodel_name='res.partner',
        
        domain=[
            ('type','!=','private'),
            ('company_id','=',False),
        ] 
    )
    
    def action_pdf(self):
        pass
    
    def action_excel(self):
        pass    