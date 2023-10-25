from odoo import models,fields,api
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools.date_utils import start_of,end_of
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta



class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    @api.constrains('request_date_from', 'request_date_to')
    def _check_something(self):
        for leave in self:
            start_date = leave.request_date_from
            end_date = leave.request_date_to

            leave_rec = self.env["hr.leave"].search([
                ('employee_id','=', self.employee_id.id),
                ('date_from', '=', end_date),
                ('date_to', '=', start_date),
                ('state','=','validate'),
            ])

            if leave_rec:
                raise UserError("LOP ERR")



    def action_done(self):
        current_date = date.today()
        first_day = start_of(current_date,"month")
        last_date = end_of(current_date,"month")
        active_emp = self.env['hr.employee'].search([('active','=',True),('contract_ids.state','=','open')])
        for employee in active_emp:
            emp_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('check_in','>=',first_day),('check_out','<=',last_date)])
            att_total = emp_attendance.mapped('check_in')

            list_a = []
            for each in att_total:#for removing the time
                list_a.append(each.date())
            month_start = first_day
            while month_start <=last_date:
                if month_start not in list_a:
                    leave_approved = self.env['hr.leave'].search([('employee_id','=',employee.id),('state','=','validate'),('request_date_from','<=',month_start),('request_date_to','>=',month_start)])
                    if month_start.strftime("%A") == 'Saturday' or month_start.strftime("%A")=='Sunday':
                        pass
                    else:
                        if not leave_approved:
                            leave = self.env['hr.leave'].create({
                                        'holiday_status_id': 5,
                                        'employee_id': employee.id,
                                        'name' : "LOP",
                                        'notes': 'LOP',
                                        'request_date_from': month_start,
                                        'date_from': month_start,
                                        'date_to': month_start,
                                        'request_date_to': month_start,
                                        'number_of_days': 1
                                        })
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',leave)
                            # leave.action_approve()
                            # leave.action_confirm()
                            leave.action_validate()
                            # date_start =
                            work_entry_type = self.env['hr.work.entry.type'].search([('code','=','LOP100')])
                            date_start = datetime(month_start.year, month_start.month, month_start.day, 9, 0, 0)

                            # Set date_stop to the end of the day (23:59:59)
                            date_stop = datetime(month_start.year, month_start.month, month_start.day, 18, 0, 0)
                            hr_work_entry_type = self.env['hr.work.entry'].search([('date_start','=',date_start.date()),('date_stop','=',date_stop.date())])
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>',hr_work_entry_type)
                            calender = self.env['hr.work.entry'].create({
                                'name': 'LOP',
                                'employee_id': employee.id,
                                # 'contract_id': ,
                                'work_entry_type_id': work_entry_type.id,
                                'date_start': date_start,
                                'date_stop' : date_stop,
                                'duration'  : 12.0,
                                'state'     : 'validated'
                            })
                            calender.action_validate()
                            # print(">>>>>>>>>>>>>>>>>>>>>>>>",calender)
                month_start += relativedelta(days=1)






