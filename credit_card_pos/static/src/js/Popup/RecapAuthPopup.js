odoo.define("credit_card_pos.RecapAuthPopup", (require) => {
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const { _lt } = require("@web/core/l10n/translation");
    
    const { onMounted, useRef, useState } = owl;

    // Definir el popup extendiendo AbstractAwaitablePopup
    const RecapAuthPopup = class extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            // Configurar el estado con ambos valores de entrada
            this.state = useState({
                recap: this.props.startingRecapValue,     // Valor inicial para RECAP
                autorizacion: this.props.startingAutorizacionValue,  // Valor inicial para Autorización
                referencia: this.props.startingReferenceValue,  // Valor inicial para Referencia
            });

            // Referencias para los campos de entrada
            this.inputRecapRef = useRef("inputRecap");
            this.inputAutorizacionRef = useRef("inputAutorizacion");
            this.inputReferenciaRef = useRef("inputReferencia");

            onMounted(this.onMounted);
        }

        onMounted() {
            // Enfocar el campo RECAP por defecto al abrir el popup
            this.inputRecapRef.el.focus();
        }

        getPayload() {
            // Retornar ambos valores de entrada (RECAP, Autorización y Referencia)
            return {
                recap: this.state.recap,
                autorizacion: this.state.autorizacion,
                referencia: this.state.referencia
            };
        }
    };

    // Asignar el nombre de la plantilla al popup
    RecapAuthPopup.template = "RecapAuthPopup";  // Asegúrate de que el nombre coincida con el del XML

    // Propiedades predeterminadas, incluyendo los nuevos campos
    RecapAuthPopup.defaultProps = {
        confirmText: _lt("Confirm"),
        cancelText: _lt("Discard"),
        title: "",
        body: "",
        startingRecapValue: "",   // Valor inicial para RECAP
        startingAutorizacionValue: "", // Valor inicial para Autorización
        startingReferenciaValue: "", // // Valor inicial para Referencia
        recapPlaceholder: _lt("Enter RECAP"),  // Placeholder para RECAP
        autorizacionPlaceholder: _lt("Enter Authorization"),  // Placeholder para Autorización
        referenciaPlaceholder: _lt("Enter Reference"),
    };

    // Registrar el componente en el registry
    Registries.Component.add(RecapAuthPopup);
});
