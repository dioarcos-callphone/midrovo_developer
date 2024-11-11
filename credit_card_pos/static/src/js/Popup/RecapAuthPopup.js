/** @odoo-module */

import AbstractAwaitablePopup from "@point_of_sale/js/Popups/AbstractAwaitablePopup";
import Registries from "@point_of_sale/js/Registries";
import { _lt } from "@web/core/l10n/translation";

const { onMounted, useRef, useState } = owl;

class RecapAuthPopup extends AbstractAwaitablePopup {  // Cambiar el nombre aquí
    setup() {
        super.setup();
        // Configurar el estado con ambos valores de entrada
        this.state = useState({
            recap: this.props.startingRecapValue,     // Valor inicial para RECAP
            autorizacion: this.props.startingAutorizacionValue,  // Valor inicial para Autorización
        });

        // Referencias para los campos de entrada
        this.inputRecapRef = useRef("inputRecap");
        this.inputAutorizacionRef = useRef("inputAutorizacion");

        onMounted(this.onMounted);
    }

    onMounted() {
        // Enfocar el campo RECAP por defecto al abrir el popup
        this.inputRecapRef.el.focus();
    }

    getPayload() {
        // Retornar ambos valores de entrada (RECAP y Autorización)
        return {
            recap: this.state.recap,
            autorizacion: this.state.autorizacion,
        };
    }
}

RecapAuthPopup.template = "RecapAuthPopup";  // Cambiar el nombre aquí

// Propiedades predeterminadas, incluyendo los nuevos campos
RecapAuthPopup.defaultProps = {
    confirmText: _lt("Confirm"),
    cancelText: _lt("Discard"),
    title: "",
    body: "",
    startingRecapValue: "",   // Valor inicial para RECAP
    startingAutorizacionValue: "", // Valor inicial para Autorización
    recapPlaceholder: _lt("Enter RECAP"),  // Placeholder para RECAP
    autorizacionPlaceholder: _lt("Enter Authorization"),  // Placeholder para Autorización
};

Registries.Component.add(RecapAuthPopup);  // Cambiar el nombre aquí

export default RecapAuthPopup;
