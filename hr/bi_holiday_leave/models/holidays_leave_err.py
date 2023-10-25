from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HolidaysErr(models.Model):
    _inherit = 'hr.leave'

#     @api.model
#     def create(self, vals):
#         date_from_str = vals.get('request_date_from')
#         date_to_str = vals.get('request_date_to')
#         date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
#         date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
#         public_holidays_leave = self.env["resource.calendar.leaves"].search([
#             ('date_from', '<=', date_to),
#             ('date_to', '>=', date_from)
#         ])
#         current_date = date_from
#         while current_date <= date_to:
#             if current_date.strftime("%A") == 'Saturday' or current_date.strftime("%A") == 'Sunday':
#                 raise UserError("Its a Saturday or Sunday")
#             current_date += relativedelta(days=1)
#         if public_holidays_leave:
#             raise UserError("Public holidays")
#         else:
#             return super(HolidaysErr, self).create(vals)
#     def write(self, vals):
#         res = super(HolidaysErr, self).write(vals)
#         date_from_str = self.request_date_from
#         date_to_str = self.request_date_to
#         date_from = date_from_str
#         date_to = date_to_str
#         public_holidays_leave = self.env["resource.calendar.leaves"].search([
#             ('date_from', '<=', date_to),
#             ('date_to', '>=', date_from)
#         ])
#         current_date = date_from
#         while current_date <= date_to:
#             if current_date.strftime("%A") == 'Saturday' or current_date.strftime("%A") == 'Sunday':
#                 raise UserError("Its a Saturday or Sunday")
#             current_date += relativedelta(days=1)
#         if public_holidays_leave:
#             raise UserError("Public holidays")
#         else:
#             return res
    @api.constrains('request_date_from','request_date_to')
    def _check_something(self):
        date_from_str = self.request_date_from
        date_to_str = self.request_date_to
        date_from = date_from_str
        date_to = date_to_str
        public_holidays_leave = self.env["resource.calendar.leaves"].search([
            ('date_from', '<=', date_to),
            ('date_to', '>=', date_from)
        ])
        current_date = date_from
        while current_date <= date_to:
            if current_date.strftime("%A") == 'Saturday' or current_date.strftime("%A") == 'Sunday':
                raise UserError("Its a Saturday or Sunday")
            current_date += relativedelta(days=1)
        if public_holidays_leave:
            raise UserError("Public holidays")
        # else:
        #     return res
        