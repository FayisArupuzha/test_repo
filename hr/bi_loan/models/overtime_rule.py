from odoo import fields,models,api

class RuleSetupOvertime(models.Model):
    _inherit ="hr.payslip"

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_input_line_ids(self):
        res = super(RuleSetupOvertime, self)._compute_input_line_ids()
        for each in self:
            if each.employee_id:
                employee = each.employee_id

                # avg_hour_salery = (self.normal_wage / self.worked_days_line_ids.number_of_days)/8

                loan_obj = self.env["overtime"].search([("employee_id", "=", employee.id),])
                date_from = each.date_from if each.date_from else date_from
                date_to = each.date_to if each.date_to else date_to

                if loan_obj:
                    existing_rule = self.struct_id.rule_ids.filtered(lambda x: x.code == "OVT100")
                    if existing_rule:
                        avg_hour_salery = 0
                        
                        for line in self.worked_days_line_ids:
                            if line.work_entry_type_id.id == 1:
                                avg_hour_salery = (self.normal_wage / line.number_of_days)/8

                        for loan in loan_obj:
                            if loan.overtime_lines_ids:
                                sum_over_time = sum(loan.overtime_lines_ids.mapped('hour')) * avg_hour_salery
                                for loan_line in loan.overtime_lines_ids:
                                    if loan_line.month <= date_to and loan_line.month >= date_from :
                                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "OVT100")], limit=1)
                                        to_add_vals = [(0, 0, {
                                            'amount': sum_over_time,
                                            'input_type_id': input_type_id.id,
                                            'name': "Over Time"
                                        })]
                                input_line_vals = to_add_vals
                                self.update({'input_line_ids': input_line_vals})
        
        return res