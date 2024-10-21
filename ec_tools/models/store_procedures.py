# -*- encoding: utf-8 -*-

from odoo import models, api, fields
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class StoreProcedure(models.AbstractModel):

    _name = 'store.procedure'
    _description = 'store.procedure'
    
    def init(self):
        #Crear lenguaje plpgsql
        #validando si ya existe no hace nada y si no existe lo crea 
        try:
            self.env.cr.execute("""
    CREATE OR REPLACE FUNCTION create_language_plpgsql()
    RETURNS BOOLEAN AS $$
        CREATE LANGUAGE plpgsql;
        SELECT TRUE;
    $$ LANGUAGE SQL;
    
    SELECT 
    CASE WHEN NOT
        (SELECT  TRUE AS exists
            FROM    pg_language
            WHERE   lanname = 'plpgsql'
         UNION
            SELECT  FALSE AS exists
            ORDER BY exists DESC
            LIMIT 1
        )
    THEN 
        create_language_plpgsql()
    ELSE
      FALSE
    END AS plpgsql_created;
      """)
        except:
            _logger.warning(_(u'Ya existe el lenguaje PLPGSQL'))
        try:
            self.env.cr.execute(""" 
    CREATE OR REPLACE FUNCTION get_field_property(text,text, integer)
    RETURNS TABLE(value text, res_model text) AS
    $BODY$
        DECLARE
            v_field_name ALIAS for $1;
            v_res_model ALIAS for $2;
            v_res_id ALIAS for $3;
            value_aux text;
            res_model_aux text;
        BEGIN
            --tomar el valor configurado para el registro
            SELECT CASE WHEN type IN ('char','text', 'selection') THEN value_text
                WHEN type = 'float' THEN CAST(value_float AS TEXT)
                WHEN type IN ('integer','integer_big') THEN CAST(value_integer AS TEXT)
                WHEN type IN ('date','datetime') THEN CAST(value_datetime AS TEXT)
                WHEN type = 'many2one' THEN CAST(split_part(value_reference,',',2) AS TEXT)
                END AS "value",
                CASE WHEN type = 'many2one' THEN CAST(SPLIT_PART(value_reference,',',1) AS TEXT)
                    ELSE ''
                END AS "res_model"
            INTO value_aux, res_model_aux
            FROM ir_property p
            LEFT JOIN ir_model_fields f ON (f.id=p.fields_id)
            WHERE f.name=v_field_name AND p.res_id = CONCAT(v_res_model,',',v_res_id);
            --si el campo no ha sido configurado, tomar el valor por defecto
            IF value_aux IS NULL THEN
                SELECT CASE WHEN type IN ('char','text', 'selection') THEN value_text
                    WHEN type = 'float' THEN CAST(value_float AS TEXT)
                    WHEN type IN ('integer','integer_big') THEN CAST(value_integer AS TEXT)
                    WHEN type IN ('date','datetime') THEN CAST(value_datetime AS TEXT)
                    WHEN type = 'many2one' THEN CAST(split_part(value_reference,',',2) AS TEXT)
                    END AS "value",
                    CASE WHEN type = 'many2one' THEN CAST(SPLIT_PART(value_reference,',',1) AS TEXT)
                        ELSE ''
                    END AS "res_model"
                INTO value_aux, res_model_aux
                FROM ir_property p
                LEFT JOIN ir_model_fields f ON (f.id=p.fields_id)
                WHERE f.name=v_field_name AND p.res_id IS NULL;
            END IF;
            RETURN QUERY SELECT value_aux AS value, res_model_aux AS res_model;
                
        END
    $BODY$
LANGUAGE 'plpgsql' VOLATILE
            """)
        except:
            _logger.warning(_(u'Error al crear el SP get_field_property'))
        try:
            self.env.cr.execute("""
    CREATE OR REPLACE FUNCTION compute_qty(integer, numeric, integer)
        RETURNS numeric AS
    $BODY$
        DECLARE
            from_oum_id ALIAS for $1;
            amount ALIAS for $2;
            to_oum_id ALIAS for $3;
            total numeric;
            f_factor numeric;
            f_factor_inv numeric;
            f_type varchar(20);
            t_factor numeric;
            t_factor_inv numeric;
            t_type varchar(20);
            t_rounding numeric;
            t_rounding_aux numeric;
            new_amount numeric;
            round_factor integer = 1;
        BEGIN
            IF from_oum_id = to_oum_id THEN
            return amount;
            ELSE
            SELECT INTO f_factor factor, f_factor_inv factor_inv, f_type uom_type 
            FROM product_uom
            WHERE id = from_oum_id;
            SELECT INTO t_factor factor, t_factor_inv factor_inv, t_rounding_aux rounding, t_type uom_type 
            FROM product_uom
            WHERE id = to_oum_id;
            t_rounding := t_rounding_aux;
            WHILE t_rounding < 1 LOOP
                t_rounding := t_rounding * 10;
                round_factor := round_factor + 1;
            END LOOP;
            new_amount := amount / f_factor;
            total := round((new_amount * t_factor), round_factor);
            END IF;
            RETURN total;
        END;
    $BODY$
    LANGUAGE plpgsql VOLATILE;                
                """)
        except:
            _logger.warning(_(u'Error al crear el SP compute_qty'))
