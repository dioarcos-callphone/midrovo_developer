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

    is_vencer = fields.Boolean('Por vencer')