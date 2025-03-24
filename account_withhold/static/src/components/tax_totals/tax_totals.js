/** @odoo-module **/

import { registry } from "@web/core/registry";
import { TaxTotalsComponent } from "@account/static/src/js/tax_totals.js";

class CustomTaxTotalsComponent extends TaxTotalsComponent {
    setup() {
        super.setup(); // Llamamos a la configuración original
        console.log("CustomTaxTotalsComponent cargado correctamente.");
    }

    /**
     * Sobreescribimos el método para agregar una nueva lógica
     */
    formatData(props) {
        let totals = JSON.parse(JSON.stringify(props.value));

        console.log(`MOSTRAR TOTALS >>> ${ totals }`)

        this.super().formatData(props)
    }
}

// Registramos el nuevo componente en Odoo
registry.category("fields").add("custom-account-tax-totals-field", CustomTaxTotalsComponent);
