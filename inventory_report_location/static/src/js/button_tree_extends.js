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
            // Llamar a la acción del informe en el backend
            const reportAction = await rpc.query({
                model: 'product.product',
                method: 'action_pdf', // El método que genera el informe PDF
                args: [], // Si necesitas pasar argumentos, agrégales aquí
            });
 
            // Verifica si la acción reportAction tiene una URL para descargar
            if (reportAction && reportAction.url) {
                // Abre la URL en una nueva pestaña (esto iniciará la descarga)
                window.open(reportAction.url, '_blank');
            } else {
                console.error("No se recibió una URL de descarga");
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