# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)


""" class PosSessionLoadFields(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result += [
            'res.config.settings',
        ]
        return result

    def _loader_params_res_config_settings(self):
        return {
            'search_params': {
                'fields': ['invoice_number_fact'],
            },
        }

    def _get_pos_ui_res_config_settings(self, params):
        return self.env['res.config.settings'].search_read(
            **params['search_params']) """


class PosOrder(models.Model):
    _inherit = 'pos.order'

    sale_barcode = fields.Char()

    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        _logger.info(f'CASHIER NAME >>> { pos_id }')
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])
        _logger.info('________ | INVOICES: %s' % invoice_id)
        _logger.info(f'CASHIER NAME >>> { invoice_id }')

        return {
            'invoice_id': invoice_id.id,
            'invoice_name': invoice_id.name,
            'invoice_number': invoice_id.l10n_latam_document_number,
            'xml_key': invoice_id.l10n_ec_authorization_number,
            'cashier_name': invoice_id.cashier_id.name


        }

