from odoo import fields, models,api
from datetime import date,datetime
from odoo.exceptions import ValidationError 
from odoo import _


class SaleorderLine(models.Model):
    _inherit="sale.order.line"


    commission = fields.Float(string="Commission %")
    commission_value = fields.Float(string="Commission Value")
    
    @api.onchange('product_id')
    def commission_percentage(self):
        for rec in self: 
            rec.commission=rec.product_id.commission

    @api.onchange('commission','price_subtotal')
    def count_commission_value(self):
        for record in self:
            record.commission_value=(record.price_subtotal*record.commission)/100






class SaleOrder(models.Model):
    _inherit="sale.order"

    commission_person_id = fields.Many2one(comodel_name="res.users",string="Commission for: ")
    total_commission=fields.Float(compute="total_commission_count",string="Commission")


    invo_sequence = fields.Char(string='Number', copy=False, readonly=False, index=True,default = lambda self: _('New'))


    def action_confirm(self):
        
        vendor_invoice=super(SaleOrder,self).action_confirm()

        # if (self.invo_sequence, _('New')) == _('New'):
        #     self.invo_sequence=self.env['ir.sequence'].next_by_code(
        #     'sale.order') or _('New') 
        #     super(libraryBooks, self).create(vals)
        # print("00000000000000000000000000000000000000000",self.invo_sequence)  
            
        values=self.env['account.move'].new({
            'move_type':'in_invoice',
            'partner_id':self.commission_person_id.partner_id.id,
            'company_id':self.company_id.id,
            'invoice_date':date.today(),
            'journal_id':2,
            'check_commission':True,

            })
        

        values._onchange_partner_id()
        print("111111111111111111111111111111111111111111111",values.id)

        values_to_write=values._convert_to_write(values._cache)

        print("+++++++++++++++++++++++++++++++++++++",values_to_write)

        create_object=self.env['account.move'].create(values_to_write)

        

            # for account move lines

        line_values=self.env['account.move.line'].new({
            'product_id':40,
            'price_unit':self.total_commission,
            'move_id':create_object.id

            })
        print("===============================",line_values['price_unit'])
        line_values._onchange_product_id()
        print("--------------------------------",line_values['price_unit'])
        
        line_values.update({
            'price_unit':self.total_commission,
            })
        line_values_to_write=line_values._convert_to_write(line_values._cache)
        # print("+++++++++++++++++++++++++++++++++++++",values)

        self.env['account.move.line'].create(line_values_to_write)


        # create_invoice=self.env['account.move'].create({
        #   'move_type':'in_invoice',
        #   'partner_id':self.commission_person_id.partner_id.id,
        #   'company_id':self.company_id.id,
        #   })  

        # self.env['account.move.line'].create({
        #   'product_id':39,
        #   'price_unit':self.total_commission,
        #   'move_id':create_invoice.id
        #   })



        create_object.action_post()
        return vendor_invoice

    def action_sale_quote_combine(self):
        partner_list=[record.partner_id.id for record in self if record.state=='draft' ]    
        partner_set=set(partner_list)
        
        if len(partner_set) == 1:
            sale_orders_records=self.env['sale.order'].search([('id','in',self.ids),
                ('state','=','draft'),('partner_id','in',partner_list)])        
            sale_order_list=[]
            for sale_object in sale_orders_records:
                for sale_object_line in sale_object.order_line:  
                    sale_order_list.append((0,0,{
                        'product_id':sale_object_line.product_id.id,
                        'product_uom_qty':sale_object_line.product_uom_qty,
                        'price_subtotal':sale_object_line.price_subtotal,
                        }))
                # sale_object.state='cancel'
                sale_object.action_cancel()

            new_sale_order=self.env['sale.order'].create({
                'partner_id':partner_list[0],
                # 'state':'sale',
                'order_line':sale_order_list
                    })
            print("=============><><><>",new_sale_order.id)
            
            new_sale_order.action_confirm()

            form_id=self.env.ref('sale.view_order_form').id 
            ctx={'order_id':new_sale_order.id}
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale Order Form',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_id,
                'res_model': 'sale.order',
                # 'domain':[('id','=',new_sale_order.id)],
                # 'context':ctx,
                'target':'new',
                }
        else:           
            raise ValidationError("Customers Are Distinct: ")
            
            
    def send_mail_sale_order(self):
        template_id=self.env.ref('supplier_invoice.email_template_for_so').id
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
           
                  }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
            # print()       

            # for record_lines in new_sale_order.order_line: 
            #   self.env['sale.order.line'].write({
            #       'order_id':new_sale_order.id,
            #       'product':
            #       })  




        
        # (21, 7, 6, 4, 3, 20, 19, 2)
        



    @api.depends('order_line.commission_value') 
    def total_commission_count(self):
        sums=0
        for count in self.order_line:
                sums+=count.commission_value
        self.total_commission=sums

