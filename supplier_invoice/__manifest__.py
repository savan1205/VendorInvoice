{
    'name': 'supplier_invoicing',
    'version': '1.0',
    'category': 'sale supplier invoicing',
    'summary': 'sale supplier invoicing',
    'sequence': -1,
    'description': """
This module contains the task of generating sale supplier invoice.
    """,
    'depends': ['sale','sale_management','product'],
    'data':[
        'security/ir.model.access.csv',

        'wizard/generate_vendor_bill.xml',
        
        'report/vendor_report.xml',
        'report/report_custom_so_action.xml',
        'report/custom_sale_report.xml',

        # 'data/custom_invoice_sequence.xml',
        
        'data/sale_order_mail.xml',
        'data/so_mail_inherit.xml',

        'views/productsView.xml',
        'views/so_line_view.xml',
        'views/account_move_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    
       
    'license': 'LGPL-3',
}
