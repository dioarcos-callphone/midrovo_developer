
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from functools import partial

from odoo import _, api, fields, models
from odoo.tools import frozendict, float_round
from odoo.tools.misc import formatLang, format_date
from odoo.exceptions import ValidationError

#from odoo.addons.l10n_ec_edi.models.account_tax import L10N_EC_TAXSUPPORTS

class accountmovepayment(models.Model):
    _inherit = "account.payment"
    def _get_default_forma_pago(self):
        #if self.env.context.get('type') == 'out_refund':
        return self.env['sri.forma.pago'].search([('code', '=', '01')])
        #return self.env.user.company_id.forma_pago_id

    l10n_ec_sri_payment_id = fields.Many2one(
        comodel_name="forma_pago_id",
        string="Payment Method (SRI)",
        default=_get_default_forma_pago,
    )

