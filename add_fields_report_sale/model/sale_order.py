from odoo import _, api, fields, models


class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'

    def get_report_matrixes(self):
        """Reporting method.

        :return: array of matrices to display in the report
        :rtype: list
        """
        matrixes = []
        # if self.report_grids:
        #     grid_configured_templates = self.order_line.filtered('is_configurable_product').product_template_id.filtered(lambda ptmpl: ptmpl.product_add_mode == 'matrix')
        #     for template in grid_configured_templates:
        #         if len(self.order_line.filtered(lambda line: line.product_template_id == template)) > 1:
        #             # TODO do we really want the whole matrix even if there isn't a lot of lines ??
        #             matrixes.append(self._get_matrix(template))
        
        return matrixes
