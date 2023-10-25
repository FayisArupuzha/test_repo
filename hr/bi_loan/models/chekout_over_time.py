from odoo import fields,models,api
from dateutil.relativedelta import relativedelta


class RuleSetupOvertime(models.Model):
    _inherit ="hr.payslip"

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_input_line_ids(self):
        res = super(RuleSetupOvertime, self)._compute_input_line_ids()
        for each in self:
            if each.employee_id:
                employee = each.employee_id
                loan_obj = self.env["hr.attendance"].search([("employee_id", "=", employee.id),])
                if loan_obj:
                    existing_rule = self.struct_id.rule_ids.filtered(lambda x: x.code == "OVT100")
                    if existing_rule:
                        avg_hour_salery = 0
                        over_time = 0
                        date_field_new = self.date_from
                        while (date_field_new <= self.date_to):
                            rec = self.env["hr.attendance"].search([])
                            new_rec = rec.filtered(lambda rec_o: rec_o.check_out.date() == date_field_new and rec_o.employee_id.id == employee.id)
                            sum_date = 0
                            for each_rec in new_rec:
                                sum_date += each_rec.worked_hours
                            if sum_date > 8:
                                over_time += sum_date - 8
                            date_field_new = date_field_new + relativedelta(days=1)
                        avg_hour_salery = 0
                        for line in self.worked_days_line_ids:
                            if line.work_entry_type_id.id == 1:
                                avg_hour_salery = (self.normal_wage / line.number_of_days)/8
                        # for loan in loan_obj:
                        sum_over_time = avg_hour_salery * over_time
                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "OVT100")], limit=1)
                        to_add_vals = [(0, 0, {
                            'amount': sum_over_time,
                            'input_type_id': input_type_id.id,
                            'name': "Over Time"
                        })]
                    input_line_vals = to_add_vals
                    self.update({'input_line_ids': input_line_vals})
        return res