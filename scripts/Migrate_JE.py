import xmlrpc.client
from datetime import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Staging2 credentials of V.8

url = 'https://sharevault-staging2-854120.dev.odoo.com'
db = 'sharevault-staging2-854120'
username = 'admin'
password = 'ju6gn5LNY6'

sv_common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
sv_common.version()
sv_uid = sv_common.authenticate(db, username, password, {})
sv_models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Production credentials of Sharevault

v13_url = 'https://odoo.sharevault.com'
v13_db = 'SV_20200515'
v13_username = 'admin'
v13_password = '!vnZD>U]9$'
v13_common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(v13_url))
v13_common.version()
v13_uid = v13_common.authenticate(v13_db, v13_username, v13_password, {})
v13_models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(v13_url))

class ImportJe:

    partner_fields = []

    def create_import_move_lines(self,values):
        list = []
        for v in values:
            account_id = False
            analytic_account_id = False
            move_line = sv_models.execute_kw(
                db, sv_uid, password, 'account.move.line', 'search_read',
                [[['id', '=', v]]],
                {'fields': ['name', 'account_id', 'debit', 'credit', 'analytic_account_id']})
            if move_line[0].get('account_id'):
                account_obj = v13_models.execute_kw(v13_db, v13_uid, v13_password, 'account.account', 'search',
            [[['code', '=', move_line[0].get('account_id')[1].split(' ')[0]]]])
                account_id = account_obj[0] if account_obj else False
            if move_line[0].get('analytic_account_id'):
                account_analytic_obj = v13_models.execute_kw(v13_db, v13_uid, v13_password, 'account.analytic.account', 'search',
                    [[['name', '=', move_line[0].get('analytic_account_id')[1]]]])
                analytic_account_id = account_analytic_obj[0] if account_analytic_obj else False
            list.append((0, 0, {
                'name': move_line[0].get('name'),
                'account_id': account_id,
                'debit': move_line[0].get('debit'),
                'credit': move_line[0].get('credit'),
                'analytic_account_id': analytic_account_id,
            }))
        return list

    def create_import_hist_lines(self, values):
        list = []
        for v in values:
            hist_line = sv_models.execute_kw(
                db, sv_uid, password, 'hist.qb.info', 'search_read',
                [[['id', '=', v]]],
                {'fields': ['hist_pqb_name', 'hist_qb_acc_type', 'hist_item', 'hist_sales_price', 'hist_qty']})
            list.append((0, 0, {'hist_pqb_name': hist_line[0].get('hist_pqb_name'),
                                'hist_qb_acc_type': hist_line[0].get('hist_qb_acc_type'),
                                'hist_item': hist_line[0].get('hist_item'),
                                'hist_sales_price': hist_line[0].get('hist_sales_price'),
                                'hist_qty': hist_line[0].get('hist_qty'),
                                }))
        return list

    def create_je(self, je):
        print('\n JEEEEEE',je)
        res = self.create_import_move_lines(je[0].get('line_ids'))
        hist_res = self.create_import_hist_lines(je[0].get('hist_qba_type_ids'))
        if je[0].get('journal_id'):
            if je[0].get('journal_id')[1] == 'Customer Invoices (USD)':
                journal = v13_models.execute_kw(v13_db, v13_uid, v13_password, 'account.journal', 'search',
                                                [[['id', '=', 1]]])
            else:
                journal = v13_models.execute_kw(v13_db, v13_uid, v13_password, 'account.journal', 'search',
                [[['id', '=', 8]]])
            if journal:
                input_date = je[0].get('date')
                date = datetime.strptime(input_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                hist_type = je[0].get('hist_type')
                hist_num = je[0].get('hist_num')
                hist_sv_name = je[0].get('hist_sv_name')
                hist_rep = je[0].get('hist_rep')
                hist_pay_method = je[0].get('hist_pay_method')
                move = v13_models.execute_kw(v13_db, v13_uid, v13_password, 'account.move', 'create', [{'date': date or False,
                                        'ref': je[0].get('ref') or False,
                                        'journal_id': journal[0],
                                        'hist_type': hist_type,
                                        'hist_num': hist_num,
                                        'hist_sv_name': hist_sv_name,
                                        'hist_rep': hist_rep,
                                        'hist_pay_method': hist_pay_method,
                                        }])
                ids = v13_models.execute_kw(v13_db, v13_uid, v13_password,'account.move', 'write',
                                        [move, {'line_ids': res,'hist_qba_type_ids': hist_res}])
                return ids

    def export_je(self):
        JE_ids = sv_models.execute_kw(
            db, sv_uid, password, 'account.move', 'search',
            [[['date', '>=', '01/01/2020'], ['date', '<=', '12/31/2020'], ['journal_id', '=', 9]]])
        created_records_list = []
        for je in JE_ids:
            je_read = sv_models.execute(db, sv_uid, password, 'account.move', 'read', je,
                                              ['ref', 'journal_id', 'date', 'hist_type', 'hist_num', 'hist_sv_name', 'hist_rep', 'hist_pay_method',
                                               'line_ids', 'hist_qba_type_ids'])
            created_records = self.create_je(je_read)
            created_records_list.append(created_records)
        print('\n final created records', created_records_list)
        print('\n final created records count',len(created_records_list))

x = ImportJe()
x.export_je()


