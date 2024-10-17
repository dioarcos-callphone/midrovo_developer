/** @odoo-module **/

import { Component } from "@odoo/owl";
import { FormStatusIndicator } from "web.FormStatusIndicator";

export class CustomFormStatusIndicator extends FormStatusIndicator {
    get displayButtons() {
        // Condición para mostrar los botones solo para un grupo específico
        const userHasGroup = this.env.services['auth_service'].isUserInGroup('your_specific_group_xml_id');
        return userHasGroup && super.displayButtons;
    }

    async discard() {
        // Lógica adicional para descartar
        if (this.shouldDiscard()) {
            await super.discard();
        } else {
            // Opcional: Mostrar un mensaje o manejar la lógica si no se puede descartar
        }
    }

    async save() {
        // Lógica adicional para guardar
        if (this.shouldSave()) {
            await super.save();
        } else {
            // Opcional: Mostrar un mensaje o manejar la lógica si no se puede guardar
        }
    }

    shouldDiscard() {
        // Tu lógica de condición para descartar cambios
        return true; // Cambia esto según tu lógica
    }

    shouldSave() {
        // Tu lógica de condición para guardar
        return true; // Cambia esto según tu lógica
    }
}

CustomFormStatusIndicator.template = "custom_security_rules.CustomFormStatusIndicator";
