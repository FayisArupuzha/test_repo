from odoo import fields,models,api

class RuleSetup(models.Model):
    _inherit ="hr.payslip"

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_input_line_ids(self):
        res = super(RuleSetup, self)._compute_input_line_ids()
        for each in self:
            if each.employee_id:
                employee = each.employee_id

                loan_obj = self.env["loan.master"].search([("employee_id", "=", employee.id), ("state", "=", "approved")])
                date_from = each.date_from if each.date_from else date_from
                date_to = each.date_to if each.date_to else date_to

                if loan_obj:
                    existing_rule = self.struct_id.rule_ids.filtered(lambda x: x.code == "EMI100")
                    if existing_rule:
                        for loan in loan_obj:
                            if loan.loan_master_lines_ids:
                                for loan_line in loan.loan_master_lines_ids:
                                    if loan_line.month <= date_to and loan_line.month >= date_from :
                                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "LOAN100")], limit=1)
                                        to_add_vals = [(0, 0, {
                                            'amount': loan_line.amount,
                                            'input_type_id': input_type_id.id,
                                            'name': "Loan - %s" % (loan_line.month.strftime('%d/%m/%Y'))
                                        })]
                                        input_line_vals = to_add_vals
                                        self.update({'input_line_ids': input_line_vals})