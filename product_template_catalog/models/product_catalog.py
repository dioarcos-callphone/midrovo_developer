from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ProductTemplateCatalog(models.Model):
    _inherit = "product.template"