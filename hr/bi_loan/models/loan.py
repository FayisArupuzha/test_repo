from odoo import fields,models,api
from dateutil.relativedelta import relativedelta



class LoanMaster(models.Model):
    _name ="loan.master"

    employee_id =  fields.Many2one('hr.employee',string='Employee',)
    number_of_install_new = fields.Integer(string='No of Installment',)

    total_amount = fields.Float(string='ammount',)
    date_field = fields.Date(string="Date")
    state = fields.Selection([
        ('draft','Draft'),
        ('approved','Approved')
    ],default='draft')
    #line page
    loan_master_lines_ids = fields.One2many('loan.master.line', 'loan_master_id', string="Loan master Line")
    

    def installment(self):
        self.write({'state':'approved'})
        
        master_lines = []
        split_month_ammount = self.total_amount / self.number_of_install_new
        date_field_new = self.date_field
        
        for rec in range(int(self.number_of_install_new)):
                new_line = self.env['loan.master.line'].create({
                    'amount' : split_month_ammount,
                    'month'  : date_field_new
                })
                date_field_new = date_field_new + relativedelta(months=1)
                master_lines.append(new_line.id)
        
        self.loan_master_lines_ids = [(6, 0, master_lines)]
    
            
        
    def set_draft(self):
        self.write({'state':'draft'})
    



