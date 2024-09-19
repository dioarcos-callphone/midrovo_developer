# -*- coding: utf-8 -*-
###############################################################################
#
#  Cybrosys Technologies Pvt. Ltd.
#
#  Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#  Author: Anusha C (odoo@cybrosys.com)
#
#  You can modify it under the terms of the GNU LESSER
#  GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#  You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#  (LGPL v3) along with this program.
#  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import fields, models


class InventoryAgingDataReport(models.TransientModel):
    """This model is for creating a wizard for viewing the report data"""
    _name = "inventory.aging.data.report"
    _description = "Informe de Datos de Envejecimiento del Inventario"

    product_id = fields.Many2one("product.product", string="Producto")
    category_id = fields.Many2one("product.category", string="Categoría")
    company_id = fields.Many2one("res.company", string="Empresa")
    qty_available = fields.Float(string="Stock Actual")
    current_value = fields.Float(string="Valor Actual")
    stock_percentage = fields.Float(string="Cantidad de Stock (%)")
    stock_value_percentage = fields.Float(string="Valor del Stock (%)")
    days_since_receipt = fields.Integer(string="Edad del Stock Más Antiguo")
    prev_qty_available = fields.Float(string="Cantidad Más Antigua")
    prev_value = fields.Float(string="Valor del Stock Más Antiguo")
    data_id = fields.Many2one('inventory.aging.report', string="Datos de Envejecimiento")
