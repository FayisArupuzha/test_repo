from odoo import models, fields,api
from dateutil.relativedelta import relativedelta

class JoiningDate(models.Model):
    _inherit = 'hr.leave'

    joining_date = fields.Date(string="Re Joining Date")

    @api.onchange('request_date_from','request_date_to')
    def joing_date(self):
        last_date = self.request_date_to
        while self.request_date_to >= last_date:
            last_date += relativedelta(days=1)
        self.joining_date =  last_date
        if last_date.strftime("%A") == 'Sunday':
            last_date += relativedelta(days=1)
            rec = self.env["resource.calendar.leaves"].search([ ('date_from', '<=', last_date),('date_to', '>=', last_date)])
            if rec:
                date = last_date
                for each in rec:
                    date = each.date_to.date()
                date +=relativedelta(days=1)
                last_date = date 
        elif last_date.strftime("%A") == 'Saturday':
            last_date += relativedelta(days=2)
            rec = self.env["resource.calendar.leaves"].search([('date_from', '<=', last_date),('date_to', '>=', last_date)])
            if rec:
                date = last_date
                for each in rec:
                    date = each.date_to.date()
                date +=relativedelta(days=1)
                last_date = date
        else:
            rec = self.env["resource.calendar.leaves"].search([ ('date_from', '<=', last_date),('date_to', '>=', last_date)])
            if rec:
                date = last_date
                for each in rec:
                    date = each.date_to.date()
                date +=relativedelta(days=1)
                last_date = date
        self.joining_date =  last_date



