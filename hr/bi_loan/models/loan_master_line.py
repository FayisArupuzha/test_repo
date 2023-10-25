from odoo import models, fields

class LoanMasterLines(models.Model):
    _name ="loan.master.line"

    month =  fields.Date(string='Date',)
    amount = fields.Float(string='Amount',)
    paid_field = fields.Boolean(string='Amount paid')
    loan_master_id = fields.Many2one("loan.master",string="Loan master",)
