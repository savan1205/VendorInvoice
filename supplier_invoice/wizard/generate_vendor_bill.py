from odoo import fields, models,api
from odoo.exceptions import ValidationError


class VendorBillWizard(models.TransientModel):
    _name = "vendor.wizard"
    _description = "create bill of Vendor"

    vendor_id = fields.Many2one(comodel_name="res.users",string="Vendor Name")


    def generate_vendor_invoice(self):
        rec_list=[]
        vendor_objects=self.env['account.move'].search([('partner_id','=',self.vendor_id.partner_id.id),('move_type','=','in_invoice')])
        # print("_____________________________________",vendor_objects.invoice_line_ids.search([]))
        # print("_____________________________________=====",vendor_objects)
        if not vendor_objects:
            raise ValidationError("record not found for vendor")
        else:    
            for rec in vendor_objects:
                if rec.check_commission == True:
                    rec_list.append(rec.id)
            return self.env.ref('supplier_invoice.action_report_vendor_invoice').report_action(rec_list)
        

      