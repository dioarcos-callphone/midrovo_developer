from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _get_data_product_variants(self):
        data_catalog = []
        data = []
        colores = []
        talla = []

        product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        
        if product_product:        
            product_attributte_lines = self.env['product.template.attribute.line'].search([(
                'product_tmpl_id', '=', self.id
            )])
            
            for product_line in product_attributte_lines:
                color = product_line.attribute_id.name
                if(color.lower() == 'color'):
                    for value in product_line.value_ids:
                        colores.append(value.name)
                        
                if(color.lower() == 'talla' or color.lower() == 'tallas'):
                    for value in product_line.value_ids:
                        talla.append(value.name)
                        
            if not colores:
                return None 
            
            if not talla:
                return None           
            
            for color in colores:
                suma_disponible = 0
                product_variants = []
                for product in product_product:
                    values = product.product_template_variant_value_ids
                    
                    if(values):
                        if(len(values) > 1):
                            for value in values:
                                val = value.name
                                if(color == val):
                                    if product.qty_available > 0:
                                        suma_disponible += int(product.qty_available)
                                        product_variants.append(product)
                                    
                        else:
                            val = values.name
                            if(color == val):
                                if product.qty_available > 0:
                                    suma_disponible += int(product.qty_available)
                                    product_variants.append(product)
                                
                            elif(values.attribute_id.name.lower() == 'tallas' or values.attribute_id.name.lower() == 'talla'):
                                if product.qty_available > 0:
                                    suma_disponible += int(product.qty_available)
                                    product_variants.append(product)
                                
                    else:
                        if product.qty_available > 0:
                            suma_disponible += int(product.qty_available)
                            product_variants.append(product)
                if product_variants:
                    product_data = {
                        "color": color,
                        "img": product_variants[0].id,
                        "tallas": product_variants,
                        "disponible": suma_disponible,
                        "talla_unica": talla
                    }

                    data.append(product_data)
            
            if data:
                for d in data:
                    product_catalogo = {}
                    tallas = d['tallas']
                    sizes = {}
                    product_catalogo['color'] = d['color']
                    product_catalogo['img'] = d['img']
                    product_catalogo['disponible'] = d['disponible']
                    product_catalogo['talla_unica'] = d['talla_unica']

                    for ta in talla:
                        for t in tallas:
                            for v in t.product_template_variant_value_ids:
                                if v.attribute_id.name.lower() in ['talla', 'tallas']:
                                    if v.name == ta:
                                        # Si la talla ya está en sizes, suma los totales
                                        if v.name in sizes:
                                            sizes[v.name] += t.qty_available
                                        else:
                                            sizes[v.name] = t.qty_available

                    # Convertir el diccionario sizes a una lista de diccionarios
                    product_catalogo['tallas'] = [{'talla': key, 'total': value} for key, value in sizes.items()]
                    data_catalog.append(product_catalogo)

        return data_catalog if data_catalog else None
    
    # @api.model
    # def validate_quantity(self, docs):
    #     longitud = len(docs)

    #     if longitud > 10:
    #         return {
    #             'name': 'Warning',
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'wizard.product.template',
    #             'view_mode': 'form',
    #             'view_id': self.env.ref('wizard_product_template_view').id,
    #             'target': 'new',
    #             'context': {'default_message': 'There are more than 10 items.'},
    #         }
        
    #     return True
