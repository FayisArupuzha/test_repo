{
    'name': 'hr employee payslip this month',
    'category': 'Hidden',
    'summary': ' payslip print',
    'version': '16.0.0.1',
    'description': """ """,
    'depends': ["hr_payroll","hr"],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
    "data": [

        "views/required_fields.xml",
        'reports/payroll_custome_header_footer.xml',
        "reports/payroll.xml",
        # "views/lop_new_shedule.xml",
        # "views/new_time_off_type.xml",
        # "views/pf_other_inputs.xml",
        # "views/tds_other_inputs.xml",
        # "views/employee_allocation_shedule.xml",

    ],
}