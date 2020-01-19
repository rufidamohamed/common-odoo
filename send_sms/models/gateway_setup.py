from odoo import _, api, fields, models, tools
from odoo.exceptions import except_orm, UserError, Warning
import requests
import urllib
import re
import logging

_logger = logging.getLogger(__name__)

class GateWaysetup(models.Model):
    _name = "gateway_setup"
    _description = "GateWay Setup"

    name = fields.Char(required=True, string='Name')
    gateway_url = fields.Char(required=True, string='GateWay Url')
    message = fields.Text('Message')
    mobile = fields.Char('Mobile')

    def send_sms_link(self,sms_rendered_content,rendered_sms_to,record_id,model,gateway_url_id):
        if rendered_sms_to:
            rendered_sms_to = re.sub(r' ', '', rendered_sms_to)
            if '+' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('+', '')
            if '-' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('-', '')


        if rendered_sms_to:
            send_url = gateway_url_id.gateway_url
            send_link = send_url.replace('{mobile}',rendered_sms_to).replace('{message}',sms_rendered_content)
            try:
                response = requests.request("GET", url = send_link).text
                return response
            except Exception as e:
                return e


    def check_error_codes(self,response):
        if '100' in response:
            raise Warning("Message has been sent successfully")

        if '101' in response:
            raise Warning("Gateway Data is not complete")

        if '102' in response:
            raise Warning("Username not correct")

        if '103' in response:
            raise Warning("Password not correct")

        if '104' in response:
            raise Warning("There is no Balance in your sms account.")

        if '104' in response:
            raise Warning("Not enough balance for sending messages")

        if '111' in response:
            raise Warning("Sending service is closed.")

        if '112' in response:
            raise Warning("112")

        if '113' in response:
            raise Warning("Account not activated")

        if '114' in response:
            raise Warning("Account is stoped")

        if '115' in response:
            raise Warning("Phone number is not activated")

        if '116' in response:
            raise Warning("Email not activated")

        if '117' in response:
            raise Warning("Message refreshed successfully")

        if '118' in response:
            raise Warning("There is no ID from message")

        if '119' in response:
            raise Warning("Faild in message removal")

        if '120' in response:
            raise Warning("Message is empty")


    @api.one
    def sms_test_action(self):
        active_model = 'gateway_setup'
        message = self.env['send.sms.template'].render_template(self.message, active_model, self.id)
        mobile_no = self.env['send.sms.template'].render_template(self.mobile, active_model, self.id)
        response = self.send_sms_link(message, mobile_no,self.id,active_model,self)
        self.check_error_codes(response)
        