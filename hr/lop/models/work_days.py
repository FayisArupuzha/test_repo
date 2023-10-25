from odoo import models,fields,api

class WorkedDays(models.Model):
    _inherit = "hr.payslip"

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_worked_days_line_ids(self):

        res = super(WorkedDays, self)._compute_worked_days_line_ids()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>lopp")

        for each in self:
            if each.employee_id:
                employee = each.employee_id
                leave_rec = self.env["hr.leave"].search([
                    ('employee_id', '=', employee.id),
                    ('date_from', '<=', self.date_to),
                    ('date_to', '>=',self.date_from),
                    ('state', '=', 'validate'),
                    ('holiday_status_id', '=', 5),
                ])
                print('??????????????????????????',leave_rec)
                work_entry_type_id = self.env['hr.work.entry.type'].search([('code', '=', "LOP100")], limit=1)
                to_add_vals = [(0, 0, {
                    'sequence': 25,
                    'work_entry_type_id': work_entry_type_id.id,
                    'number_of_days': len(leave_rec),
                    'number_of_hours':len(leave_rec)* 8,
                    # 'employee_id' : employee.id,
                    'amount' : 100,
                })]
                input_line_vals = to_add_vals
                self.update({'worked_days_line_ids': input_line_vals})
                print(">@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@lop",input_line_vals)

        return res

        @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
        def _get_worked_day_lines(self, domain=None, check_out_of_contract=True):
            res = super(WorkedDays,self)._get_worked_day_lines()
            print('dsfkjs')
            return res
