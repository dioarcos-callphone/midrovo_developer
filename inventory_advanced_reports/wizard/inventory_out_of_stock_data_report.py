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


class InventoryOutOfStockDataReport(models.TransientModel):
    """This model is for creating a wizard for viewing the report data"""
    _name = "inventory.out.of.stock.data.report"
    _description = "Análisis de inventario agotado"

    product_id = fields.Many2one("product.product", string="Producto")
    category_id = fields.Many2one("product.category", string="Categoría")
    company_id = fields.Many2one("res.company", string="Empresa")
    warehouse_id = fields.Many2one("stock.warehouse", string="Almácen")
    virtual_stock = fields.Float(string="Cantidad pronosticada")
    sales = fields.Float(string="Ventas")
    ads = fields.Float(string="ADS")
    demanded_quantity = fields.Float(string="Cantidad demandada")
    in_stock_days = fields.Float(string="Días en stock")
    out_of_stock_days = fields.Float(string="Días de agotamiento")
    out_of_stock_ratio = fields.Float(string="Índice de agotamiento")
    cost = fields.Float(string="Precio de costo")
    out_of_stock_qty = fields.Float(string="Cantidad agotada")
    out_of_stock_qty_percentage = fields.Float(string="Porcentaje de cantidad agotada")
    out_of_stock_value = fields.Float(string="Porcentaje del valor agotado")
    turnover_ratio = fields.Float(string="Índice de rotación")
    fsn_classification = fields.Char(string="Clasificación FSN")
    data_id = fields.Many2one('inventory.out.of.stock.report',
                              string="Datos de agotamiento")
