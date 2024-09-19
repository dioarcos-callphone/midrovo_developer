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


class InventoryFsnXyzDataReport(models.TransientModel):
    """This model is for creating a wizard for viewing the report data"""
    _name = "inventory.fsn.xyz.data.report"
    _description = "Informe de datos de inventario FSN-XYZ"

    product_id = fields.Many2one("product.product", string="Producto")
    category_id = fields.Many2one("product.category", string="Categoría")
    company_id = fields.Many2one("res.company", string="Empresa")
    average_stock = fields.Float(string="Stock Promedio")
    sales = fields.Float(string="Ventas")
    turnover_ratio = fields.Float(string="Índice de rotación")
    current_stock = fields.Float(string="Stock actual")
    stock_value = fields.Float(string="Valor de inventario")
    fsn_classification = fields.Char(string="Clasificación FSN")
    xyz_classification = fields.Char(string="Clasificación XYZ")
    combined_classification = fields.Char(string="Clasificación FSN-XYZ")
    data_id = fields.Many2one('inventory.fsn.xyz.report', string="Datos FSN-XYZ")
