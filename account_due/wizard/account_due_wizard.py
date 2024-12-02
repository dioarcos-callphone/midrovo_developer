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
    
    journal_id = fields.Many2one(
        string = 'Diario',
        comodel_name='account.journal',
        domain=[('type','=','sale')] 
    )
    
    comercial_ids = fields.Many2one(
        string = 'Comercial',
        comodel_name='res.users'
    )
    
    def action_pdf(self):
        data = {
            'model_id': self.id,
            'court_date': self.court_date,
            'client_id': self.client_id.id,
        }
        
        return (
            self.env.ref(
                'invoice_details_view.report_invoice_details_action'
            )
            .report_action(None, data=data)
        )
    
    def action_excel(self):
        pass    