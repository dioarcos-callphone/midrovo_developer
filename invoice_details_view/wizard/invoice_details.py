from odoo import models, fields, api
from odoo.exceptions import ValidationError

class InvoiceDetails(models.TransientModel):
    _name = "invoice.details.wizard"
    _description = "Informe de Detalles de las Facturas"
    
    start_date = fields.Date(
        string = 'Fecha de inicio',
        help = 'Fecha de inicio para analizar el informe',
        required = True
    )
    
    end_date = fields.Date(
        string = 'Fecha de fin',
        help = 'Fecha de fin para analizar el informe',
        required = True
    )
    
    journal_ids = fields.Many2many(
        string = 'Diario',
        comodel_name='account.journal',
    )
    
    comercial_ids = fields.Many2many(
        string = 'Comercial',
        comodel_name='res.users'
    )
    
    def action_pdf(self):
        if self.start_date > self.end_date:
            raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin")
        return
    
    