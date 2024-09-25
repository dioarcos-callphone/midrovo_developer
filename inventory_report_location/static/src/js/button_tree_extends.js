/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class SaleListController extends ListController {
   setup() {
       super.setup();
   }
   async actionPDF() {
    try {
        // Llamar al método action_pdf sin pasar ningún argumento
        const { data } = await this._rpc({
            model: 'product.product',
            method: 'action_pdf',
            args: [],  // No se pasan argumentos ya que no hay selección
        });

        // Manejar la respuesta para abrir el PDF
        if (data && data.pdf_url) {
            window.open(data.pdf_url, '_blank');
        } else {
            this._notify("Error al generar el PDF", { type: "warning" });
        }
    }
    
    catch (error) {
        console.error("Error al ejecutar actionPDF:", error);
        this._notify("Ocurrió un error al generar el PDF", { type: "danger" });
    }

   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});