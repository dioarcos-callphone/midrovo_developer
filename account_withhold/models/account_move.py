from odoo import _, api, fields, models
from odoo.tools.misc import formatLang

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'account.move'

    @api.depends('country_code', 'line_ids.tax_ids.tax_group_id', 'line_ids.l10n_ec_withhold_tax_amount', 'line_ids.balance')
    def _compute_l10n_ec_withhold_subtotals(self):
        _logger.info("ENTRA EN EL METODO COMPUTADO")
        def line_dict(withhold_line):
            return {
                'tax_group': withhold_line.tax_ids.tax_group_id,
                'amount': withhold_line.l10n_ec_withhold_tax_amount,
                'base': abs(withhold_line.balance),
            }

        moves_ec = self.filtered(lambda move: move.country_code == 'EC')
        (self - moves_ec).l10n_ec_withhold_subtotals = False
        for move in moves_ec:
            if move.l10n_ec_withhold_type:
                lines = move.l10n_ec_withhold_line_ids.mapped(line_dict)
                move.l10n_ec_withhold_subtotals = self._l10n_ec_withhold_subtotals_dict(move.currency_id, lines)
            else:
                move.l10n_ec_withhold_subtotals = {}

    @api.model
    def _l10n_ec_withhold_subtotals_dict(self, currency_id, lines):
        _logger.info('ENTRA EN EL METODO SUBTOTALS DICT')

        """
        This method returns the information for the tax summary widgets in both the withhold wizard as in the withholding
        itself. That is why the lines are passed as parameter.
        """
        vat_amount, pro_amount, vat_base, pro_base = 0.0, 0.0, 0.0, 0.0
        vat_tax_group, pro_tax_group = None, None
        for line in lines:
            tax_group_id = line['tax_group']
            if tax_group_id:
                if tax_group_id.l10n_ec_type in ['withhold_vat_sale', 'withhold_vat_purchase']:
                    vat_tax_group = tax_group_id
                    vat_amount += line['amount']
                    vat_base += line['base']
                elif tax_group_id.l10n_ec_type in ['withhold_income_sale', 'withhold_income_purchase']:
                    pro_tax_group = tax_group_id
                    pro_amount += line['amount']
                    pro_base += line['base']

        if not (vat_tax_group or pro_tax_group):
            _logger.info("RETORNA FALSE")
            return False  # widget gives errors if no tax groups

        wth_subtotals = {
            'formatted_amount_total': formatLang(self.env, vat_amount + pro_amount, currency_obj=currency_id),
            'allow_tax_edition': False,
            'groups_by_subtotal': {},
            'subtotals_order': [],
            'subtotals': [],
            'display_tax_base': False,
        }

        def add_subtotal(amount, base, currency, key):
            # Add a subtotal to the widget
            # We need to add a group_by_subtotal, subtotals and subtotals_order otherwise the widget will crash
            formatted_base = formatLang(self.env, base, currency_obj=currency)
            wth_subtotals['groups_by_subtotal'][key] = []
            wth_subtotals['subtotals_order'].append(key)
            wth_subtotals['subtotals'].append({
                'name': key,
                'formatted_amount': _('(base: %s) %s', formatted_base, formatLang(self.env, amount, currency_obj=currency))
            })

        if vat_tax_group:
            add_subtotal(vat_amount, vat_base, currency_id, _("VAT Withhold"))
        if pro_tax_group:
            add_subtotal(pro_amount, pro_base, currency_id, _("Profit Withhold"))

        
        _logger.info(f'SE RETORNA WTH SUBTOTALS >>> { wth_subtotals }')

        return wth_subtotals
    