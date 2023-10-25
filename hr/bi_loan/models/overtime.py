from odoo import fields,models,api
from dateutil.relativedelta import relativedelta

class OverTime(models.Model):
    _name ="overtime"

    employee_id =  fields.Many2one('hr.employee',string='Employee',)
    number_of_hour_worked = fields.Integer(string='Over Time',)
    number_of_hour_days= fields.Integer(string='Number of days',)
    date_field = fields.Date(string="Date")
  
    #line page
    overtime_lines_ids = fields.One2many('overtime.line', 'overtime_master_id', string="over time  Line connection ids")
    

    def installment_1(self):
        # self.write({'state':'approved'})
        
        master_lines = []
        date_field_new = self.date_field
        
        for rec in range(int(self.number_of_hour_days)):
                new_line = self.env['overtime.line'].create({
                    'month' : date_field_new,
                    'hour'  : self.number_of_hour_worked
                })
                date_field_new = date_field_new + relativedelta(days=1)
                master_lines.append(new_line.id)
        
        self.overtime_lines_ids = [(6, 0, master_lines)]
    
            
        
    # def set_draft(self):
    #     self.write({'state':'draft'})
    


class OverTimeLine(models.Model):
    _name ="overtime.line"

    month =  fields.Date(string='Date')
    hour = fields.Integer(strring="Hour")
    overtime_master_id = fields.Many2one("overtime",string="over time id",)
