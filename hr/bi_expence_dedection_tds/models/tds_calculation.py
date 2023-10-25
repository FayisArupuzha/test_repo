from odoo import fields,models,api

class TdsCalculation(models.Model):
    _name ="account.tds"
    employee_id = fields.Many2one('hr.employee',string="Employee")
    tds_amount = fields.Float(string='TDS Amount Year')
    tds_amount_month = fields.Float(string="TDS Amount Month ")
    Gross_salary = fields.Float(string=' Year wise Salary')
    Gross_salary_month = fields.Float(string=' Month wise Salary')
    expense = fields.Float(string='Monthly expense')

    line_ids = fields.One2many('account.tds.line','line_id',string="Line ids")



    #tax slab 
    yearly_salary = fields.Float(string= "Yearly salary after expense")
    tax = fields.Float (string ="tax percentage ")
    year_connection_id = fields.Many2one('account.tds.setup',string='Year Of tax Slab')

    @api.onchange('year_connection_id')
    def tax_slab(self):
        yearly_salary = self.Gross_salary
        tds_percentage = 0.00
        for line in self.year_connection_id.line_ids:
            if yearly_salary >= line.amount_from and yearly_salary <= line.amount_to:
                tds_percentage = line.tax_percentage
                break

        self.tax = tds_percentage
        # self.line_ids = [(5, 0, 0)]  # Unlink all existing records
        # line_ids = []
        # for line in self.year_connection_id.line_ids:
        #     line_ids.append((0, 0, {
        #         'amount_from': line.amount_from,  # Replace 'field1' with the actual field names in your 'account.tds.line' model
        #         'amount_to': line.amount_to,
        #         'tax_percentage': line.tax_percentage,

        #         # Add other fields here
        #     }))
        # self.line_ids = line_ids
        # self.line_ids = self.year_connection_id.line_ids



    @api.onchange('tax')
    def Calculation_tds_tax(self):
       
        self.tds_amount = (self.yearly_salary * self.tax) / 100
        self.tds_amount_month = ((self.yearly_salary * self.tax) / 100) / 12

        contract = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
        contract.update({'tds': self.tds_amount_month})
        # contract

    @api.onchange('employee_id')
    def Calculation_tds(self):
        contract = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
        self.Gross_salary = contract.wage * 12
        self.yearly_salary = (contract.wage - (contract.wage * 1.5) / 100) * 12
        self.Gross_salary_month = contract.wage
        self.expense = (contract.wage * 1.5) / 100 
        # if contract.wage * 12 <= 250000:
        #     self.tds_amount = 0
        #     self.tds_amount_month = 0

        # elif contract.wage * 12 >= 250001 and contract.wage * 12 <= 500000:
        #     self.tds_amount = ((contract.wage * 5) / 100 - (contract.wage * 1.5) / 100)*12
        #     self.tds_amount_month = (contract.wage * 5) / 100 - (contract.wage * 1.5) / 100

        # elif contract.wage * 12 >= 500001 and contract.wage * 12 <= 1000000:
        #     self.tds_amount =(12500 /12 + (contract.wage * 20) / 100 - (contract.wage * 1.5) / 100)*12
        #     self.tds_amount_month = (12500 /12 + (contract.wage * 20) / 100 - (contract.wage * 1.5) / 100)

        # elif contract.wage * 12 >1000000:
        #     self.tds_amount =(112500 /12 + (contract.wage * 30) / 100 - (contract.wage * 1.5) / 100)*12
        #     self.tds_amount_month = (112500 /12 + (contract.wage * 30) / 100 - (contract.wage * 1.5) / 100)


class TdsCalculationLine(models.Model):
    _name ="account.tds.line"
    line_id = fields.Many2one('account.tds',string='line id')

    amount_from = fields.Float(string='Amount From')
    amount_to = fields.Float(string='Amount To')
    tax_percentage = fields.Float(string='Tax')


