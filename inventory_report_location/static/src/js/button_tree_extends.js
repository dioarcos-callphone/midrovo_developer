/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import rpc from "web.rpc";
export class SaleListController extends ListController {
    setup() {
       super.setup();
    }
    
    async actionPDF() {
        try {
            // Hacer una llamada al controlador
            const result = await rpc({
                route: '/product/pdf_report',
                params: {}, // Aquí puedes enviar parámetros si lo necesitas
            });

            // La respuesta de la acción PDF puede redirigir a la URL de descarga
            if (result) {
                // Aquí puedes redirigir a la URL de descarga del PDF si es necesario
                window.open(result, '_blank'); // Abre en una nueva pestaña
            }
        } catch (error) {
            console.error("Error al generar el PDF:", error);
        }
    }
}

registry.category("views").add("button_in_tree", {
    ...listView,
    Controller: SaleListController,
    buttonTemplate: "button_sale.ListView.Buttons",
});