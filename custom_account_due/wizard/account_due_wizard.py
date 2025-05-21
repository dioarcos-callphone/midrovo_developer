import io
import json
from datetime import datetime
from odoo import models, fields
from odoo.exceptions import ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

import logging
_logger = logging.getLogger(__name__)

class AccountDueWizard(models.TransientModel):
    _inherit = "account.due.wizard"

    analysis_receivable_balance = fields.Selection(
        [
            ('vencer', 'Saldo por vencer'),
            ('vencido', 'Saldo vencido'),
        ],
        string = 'Analisis de Reporte de Saldo',
        default = 'vencido',
        help = "Seleccione el analisis de saldo por cobrar"
    )