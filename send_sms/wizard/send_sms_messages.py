# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from datetime import datetime






class SMSComposer(models.Model):
    _name = 'sms.send.messages'
    _description = 'SMS Send messages'

    @api.depends('partner_type')
    def get_model_name_sms(self):
        for rec in self:
            rec.name = rec.partner_type +'/' + rec.sending_time


    name = fields.Char(string="Name",compute="get_model_name_sms")
    partner_type = fields.Selection(
        string='Partner Type',
        selection=[('customer', 'Customers'), ('supplier', 'Vendors')],default='customer',
        required=True
        
    )

    sending_time = fields.Selection(
        string='Sending Type',
        selection=[('now', ' send now'), ('later', 'at specific time')],default='now',
        required=True
        
    )

    
    sending_date = fields.Datetime(
        string='Sending Date',
        default=fields.Datetime.now,
        required=True
        
    )
    
    
    template_id = fields.Many2one('send.sms.template', 'SMS Template',
    required=True
    )
    partner_ids = fields.Many2many('res.partner',
    )

    state = fields.Selection([
            ('draft', 'Draft'),
            ('schedule', 'Scheduled'),
            ('send', 'Sent'),
            ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, default='draft')

    
    @api.onchange('partner_type')
    def _onchange_partner_type(self):
        lines =[]
    
        if self.partner_type =='customer':
            Customers = self.env['res.partner'].search([('customer','=',True)])
            lines.append((6,0, Customers.ids))
            self.update({'partner_ids': lines})
        else:
            Customers = self.env['res.partner'].search([('supplier','=',True)])
            lines.append((6,0, Customers.ids))        
            self.update({'partner_ids': lines})
    

    def action_delete_lines(self):
        for rec in self:
            self.partner_ids = [(5, 0, 0)]

    def action_send(self):
        for rec in self:
            rec.state = 'send'

    def action_scheduled(self):
        for rec in self:
            rec.state = 'schedule'

    def action_cancelled(self):
        for rec in self:
            rec.state = 'cancel' 

    def action_rest_draft(self):
        for rec in self:
            rec.state = 'draft'                
    
    

    @api.multi
    def send_messages_action(self):

        for record in self.partner_ids :
            if not record.phone:
                raise UserError(_('You must specify phone number for this partner : %s' , partner_ids.dispaly))
        num_list = []
        number_list = []
        for line in self.partner_ids :
            num_list.append(line.phone)
        
        number_list = ','.join(num_list)
        
        self.env['send.sms.template'].send_sms(self.id, self.template_id, number_list )


    @api.multi
    def scheduler_message_action(self):
        
        scheduled = self.search([('state','=','schedule')])
        for record in scheduled:
            #prepare vars to convert phones to string and pass to send_sms method
            phones_list = []
            phones_string = ""
         
            sending_date = record.sending_date.date() 
            now = datetime.now().date()

            if now == sending_date:
                    
                if record.partner_ids:

                    for rec in record.partner_ids:
                        if rec.phone:
                            phones_list.append(rec.phone)

                    phones_string=','.join(phones_list)

                temp_id = record.template_id

                
                self.env['send.sms'].send_sms(self.id, temp_id, phones_string)



        