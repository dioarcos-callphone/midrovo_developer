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


class InventoryOverStockDataReport(models.TransientModel):
    """This model is for creating a wizard for viewing the report data"""
    _name = "inventory.over.stock.data.report"
    _description = "Análisis de excedente de inventario"

    product_id = fields.Many2one("product.product", string="Producto")
    category_id = fields.Many2one("product.category", string="Categoría")
    company_id = fields.Many2one("res.company", string="Empresa")
    warehouse_id = fields.Many2one("stock.warehouse", string="Almacén")
    virtual_stock = fields.Float(string="Cantidad pronosticada")
    sales = fields.Float(string="Ventas")
    ads = fields.Float(string="ADS")
    demanded_quantity = fields.Float(string="Cantidad demandada")
    in_stock_days = fields.Float(string="Días de cobertura")
    over_stock_qty = fields.Float(string="Cantidad excedente")
    over_stock_qty_percentage = fields.Float(string="Porcentaje de cantidad excedente")
    over_stock_value = fields.Float(string="Valor del excedente")
    over_stock_value_percentage = fields.Float(string="Porcentaje del valor del excedente")
    turnover_ratio = fields.Float(string="Índice de rotación")
    fsn_classification = fields.Char(string="Clasificación FSN")
    po_date = fields.Datetime(string="Fecha de la última orden de compra")
    po_qty = fields.Float(string="Última cantidad de pedido")
    po_price_total = fields.Float(string="Precio del último pedido de compra")
    po_currency_id = fields.Many2one("res.currency", string="Divisa")
    po_partner_id = fields.Many2one("res.partner", string="Socio")
    data_id = fields.Many2one('inventory.over.stock.report',
                              string="Datos de excedente de inventario")
