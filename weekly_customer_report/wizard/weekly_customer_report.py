# -*- coding: utf-8 -*-

from odoo import models, fields,api, _
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter


class WeeklyCustomerReport(models.TransientModel):
    _name = "weekly.customer.report"
    _description = "Weekly Customer Report"

    @api.model
    def _get_domain_partner(self):
        res_list = []
        account_move = self.env['account.move'].search([('state', '=', 'posted'), ('type', '=', 'out_invoice')])
        for move in account_move:
            if move.sharevault_id:
                if move.partner_id.is_company:
                    res_list.append(move.partner_id.id)
        if res_list:
            return [('id', 'in', res_list)]

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    partner_ids = fields.Many2many('res.partner', string='Customers', domain=_get_domain_partner)
    select_all = fields.Boolean('Select All Customer')

    @api.onchange('select_all')
    def _onchange_select_all(self):
        if self.select_all:
            self.partner_ids = False

    @api.constrains('from_date', 'to_date')
    def check_date(self):
        """ This method is used to check constrains on dates."""
        if self.from_date and self.to_date and (self.from_date > self.to_date):
            raise ValidationError(_('To Date should be greater than From Date.'))

    def get_total(self, id):
        total = 0
        if self.to_date and self.from_date:
            invoices_recs = self.env['account.move'].search(
                [('state', '=', 'posted'), ('type', '=', 'out_invoice'), ('invoice_date', '<=', self.to_date),
                 ('invoice_date', '>=', self.from_date),('sharevault_id', '=', id)])
            for inv in invoices_recs:
                for line in inv.invoice_line_ids:
                    total += line.price_subtotal
        else:
            invoices_recs = self.env['account.move'].search(
                [('sharevault_id', '=', id), ('state', '=', 'posted'), ('type', '=', 'out_invoice')])
            for inv in invoices_recs:
                for line in inv.invoice_line_ids:
                    total += line.price_subtotal
        return total

    def get_customer_total(self, id):
        partner = self.env['res.partner'].browse(id)
        sharevault_ids = partner.sharevault_c_ids.ids
        total = 0
        if self.to_date and self.from_date:
            invoices_recs = self.env['account.move'].search(
                [('state', '=', 'posted'), ('type', '=', 'out_invoice'), ('invoice_date', '<=', self.to_date),
                 ('invoice_date', '>=', self.from_date),('sharevault_id', 'in', sharevault_ids)])
            for inv in invoices_recs:
                total += inv.amount_total
        else:
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
        return list(set(sharevault_ids))

    def print_xls(self):
        if self.partner_ids:
            partners = self.env['res.partner'].search([('id', 'in', self.partner_ids.ids)])
        if self.select_all:
            res_list = []
            account_move = self.env['account.move'].search([('state', '=', 'posted'), ('type', '=', 'out_invoice')])
            for move in account_move:
                if move.sharevault_id:
                    if move.partner_id.is_company:
                        res_list.append(move.partner_id.id)
            partners = self.env['res.partner'].search([('id', 'in', list(set(res_list)))])
        if self.to_date and self.from_date and self.partner_ids:
            res_list = []
            account_move = self.env['account.move'].search(
                [('state', '=', 'posted'), ('type', '=', 'out_invoice'), ('invoice_date', '<=', self.to_date),
                 ('invoice_date', '>=', self.from_date), ('partner_id','in',self.partner_ids.ids)])
            for move in account_move:
                if move.sharevault_id:
                    if move.partner_id.is_company:
                        res_list.append(move.partner_id.id)
            partners = self.env['res.partner'].search([('id', 'in', list(set(res_list)))])
        if self.to_date and self.from_date and self.select_all:
            res_list = []
            account_move = self.env['account.move'].search(
                [('state', '=', 'posted'), ('type', '=', 'out_invoice'), ('invoice_date', '<=', self.to_date),
                 ('invoice_date', '>=', self.from_date)])
            for move in account_move:
                if move.sharevault_id:
                    if move.partner_id.is_company:
                        res_list.append(move.partner_id.id)
            partners = self.env['res.partner'].search([('id', 'in', list(set(res_list)))])
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
        row += 1
        colm = 0
        if not partners:
            raise ValidationError(_('Record Not found'))
        for partner in partners:
            worksheet.write(row, colm, partner.name, body)
            row += 1
            colm += 1
            sharevault_c_ids = self._check_sharevault_records(partner)
            for sv in sharevault_c_ids:
                sharevault = self.env['sharevault.sharevault'].browse(sv)
                invoices_recs = self.env['account.move'].search([('sharevault_id', '=', sv)])
                if self.to_date and self.from_date:
                    invoices_recs = self.env['account.move'].search(
                        [('sharevault_id', '=', sv), ('invoice_date', '<=', self.to_date),
                         ('invoice_date', '>=', self.from_date)])
                if invoices_recs:
                    worksheet.write(row, colm, sharevault.sharevault_name, body)
                    row += 1
                    colm += 1
                for inv in invoices_recs.filtered(lambda p: p.type == "out_invoice" and p.state == 'posted'):
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
                if invoices_recs:
                    colm = 1
                    worksheet.write(row, colm, 'Total '+str(sharevault.sharevault_name), body)
                    worksheet.write(row, colm + 8, self.get_total(sv), body)
                    row += 1
                    colm = 1
            colm = 0
            worksheet.write(row, colm, 'Total ' + str(partner.name), body)
            worksheet.write(row, colm + 9, self.get_customer_total(partner.id), body)
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