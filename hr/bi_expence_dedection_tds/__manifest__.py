{
    'name': 'Odoo 16 Tds calculation',
    'author': 'Fayis',
    'category': 'hr',
    'version': '16.0.0.1',
    'description': """ """,
    'summary': 'new filed creation in odoo.sale',
    # 'sequence': 11,
    # 'website': 'https://www.odoomates.tech',
    'depends': ['hr_holidays','hr','hr_payroll','hr_contract'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/tds_calculation.xml',  
        'views/hr_contract.xml',
        'views/tds_setup.xml',
       
        
        
    ],
}    