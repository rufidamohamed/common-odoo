{
    'name': "Send SMS",
    'version': '0.1',
    'author': "Debasish Dash",
    'category': 'Tools',
    'summary':'You can use multiple gateway for multiple sms template to send SMS.',
    'description':'Allows you to send SMS to the mobile no.',
    'website': "http://www.debweb.com",
    'depends': ['base','web',],
    'data': [
        'security/ir.model.access.csv',
        'security/sms_groups.xml',
        'view/send_sms_view.xml',
        'view/ir_actions_server_views.xml',
        'view/sms_track_view.xml',
        'view/gateway_setup_view.xml',
        'wizard/sms_compose_view.xml',
        'wizard/send_sms_send_sms_messages_view.xml',
        'wizard/scheduler_message_action.xml'
        
    ],
    'images':['static/description/banner.png'],
    # 'license': 'LGPL-3',
    'installable':True,
    'auto_install':False,
}
