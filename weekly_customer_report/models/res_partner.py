# -*- coding: utf-8 -*-
from odoo import models, fields,api, _
import base64
import io
import xlsxwriter
from odoo.exceptions import Warning,ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def get_total(self, id):
        invoices_recs = self.env['account.move'].search(
            [('sharevault_id', '=', id), ('state', '=', 'posted'), ('type', '=', 'out_invoice')])
        total = 0
        for inv in invoices_recs:
            for line in inv.invoice_line_ids:
                total += line.price_subtotal
        return total

    def get_customer_total(self, id):
        total = 0
        for partner in self.browse(id):
            sharevault_ids = partner.sharevault_c_ids.ids
            invoices_recs = self.env['account.move'].search(
                [('partner_id', '=', partner.id), ('state', '=', 'posted'), ('type', '=', 'out_invoice'),
                 ('sharevault_id', 'in', sharevault_ids)])
            for inv in invoices_recs:
                total += inv.amount_total
        return total

    def get_inv_type(self, type):
        if type == 'out_invoice':
            return 'Invoice'
        if type == 'in_invoice':
            return 'Bill'
        else:
            return ''

    def _check_sharevault_records(self, partner):
        account_move = self.env['account.move'].search(
            [('partner_id', '=', partner.id), ('state', '=', 'posted'), ('type', '=', 'out_invoice')])
        sharevault_ids = []
        for move in account_move:
            if move.sharevault_id:
                sharevault_ids.append(move.sharevault_id.id)
        return sharevault_ids

    def get_weekly_report(self):
        for partner_rec in self:
            fp = io.BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            worksheet = workbook.add_worksheet('Weekly Customer Report')
            header_format = workbook.add_format({'bold': True, 'align': 'left', 'color': 'black'})
            body = workbook.add_format({'align': 'left', 'color': 'black'})
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 30)
            worksheet.set_column('C:C', 10)
            worksheet.set_column('D:D', 10)
            worksheet.set_column('E:E', 10)
            worksheet.set_column('F:F', 17)
            worksheet.set_column('G:G', 40)
            worksheet.set_column('H:H', 20)
            worksheet.set_column('I:I', 10)
            worksheet.set_column('J:J', 10)
            not_exist = workbook.add_format({'bold': True, 'font_color': 'red'})
            row = 0
            colm = 0
            worksheet.write(row, colm, 'Customer', header_format)
            colm += 1
            worksheet.write(row, colm, 'ShareVault', header_format)
            colm += 1
            worksheet.write(row, colm, 'Type', header_format)
            colm += 1
            worksheet.write(row, colm, 'Date', header_format)
            colm += 1
            worksheet.write(row, colm, 'Num', header_format)
            colm += 1
            worksheet.write(row, colm, 'Name Account #', header_format)
            colm += 1
            worksheet.write(row, colm, 'Memo', header_format)
            colm += 1
            worksheet.write(row, colm, 'Product Code', header_format)
            colm += 1
            worksheet.write(row, colm, 'Rep', header_format)
            colm += 1
            worksheet.write(row, colm, 'Amount', header_format)
            if partner_rec:
                row += 1
                colm = 0
                worksheet.write(row, colm, partner_rec.name, body)
                row += 1
                colm += 1
                if not partner_rec.sharevault_c_ids:
                    raise ValidationError(_('ShareVaults not found for this customer'))
                sharevault_c_ids = self._check_sharevault_records(partner_rec)
                if not sharevault_c_ids:
                    raise ValidationError(_('ShareVault is not selected in related invoices of this customer'))
                for sv in sharevault_c_ids:
                    sharevault = self.env['sharevault.sharevault'].browse(sv)
                    worksheet.write(row, colm, sharevault.sharevault_name, body)
                    row += 1
                    colm += 1
                    invoices_recs = self.env['account.move'].search(
                        [('sharevault_id', '=', sv), ('state', '=', 'posted'), ('type', '=', 'out_invoice')])
                    for inv in invoices_recs:
                        for line in inv.invoice_line_ids:
                            worksheet.write(row, colm, self.get_inv_type(line.move_id.type), body)
                            colm += 1
                            worksheet.write(row, colm, line.move_id.invoice_date.strftime('%m/%d/%Y'), body)
                            colm += 1
                            worksheet.write(row, colm, line.move_id.ref, body)
                            colm += 1
                            worksheet.write(row, colm, line.account_id.name, body)
                            colm += 1
                            worksheet.write(row, colm, line.move_id.invoice_payment_ref, body)
                            colm += 1
                            worksheet.write(row, colm, line.product_id.default_code, body)
                            colm += 1
                            worksheet.write(row, colm, line.move_id.rep_id.name, body)
                            colm += 1
                            worksheet.write(row, colm, line.price_subtotal, body)
                            row += 1
                            colm = 2
                    colm = 1
                    worksheet.write(row, colm, 'Total '+str(sharevault.sharevault_name), body)
                    worksheet.write(row, colm + 8, self.get_total(sv), body)
                    row += 1
                    colm = 1
                colm = 0
                worksheet.write(row, colm, 'Total ' + str(partner_rec.name), body)
                worksheet.write(row, colm + 9, self.get_customer_total(partner_rec.id), body)
                row += 1
                colm = 0

            workbook.close()
            fp.seek(0)
            result = base64.b64encode(fp.read())
            attachment_obj = self.env['ir.attachment']
            attachment_id = attachment_obj.create(
                {'name': 'weekly_customer_report.xlsx',
                 'datas': result})
            download_url = '/web/content/' + \
                           str(attachment_id.id) + '?download=True'
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            return {
                "type": "ir.actions.act_url",
                "url": str(base_url) + str(download_url),
                "target": "new"
            }