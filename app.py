# ==========================================
#   💳 حسابداری حرفه‌ای - نسخه دسکتاپ
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox
import json, os, hashlib, secrets, hmac, random
from datetime import datetime, timedelta

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, 'data.json')

C = {
    'primary': '#6C63FF', 'primary_dark': '#5A52D5',
    'success': '#00B894', 'danger': '#FF6B6B',
    'warning': '#FDCB6E', 'info': '#74B9FF',
    'bg': '#F0F2F5', 'white': '#FFFFFF',
    'text': '#2D3436', 'text_light': '#636E72',
    'border': '#E8E8EE', 'hover': '#F5F6FA'
}

data = {'users': [], 'accounts': [], 'transactions': [],
        'nextUserId': 1, 'nextAccountId': 1, 'nextTxId': 1}

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data.update(json.load(f))
    except:
        pass


def save():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass


def hash_password(p):
    s = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac('sha256', p.encode(), s.encode(), 100000)
    return f"{s}:{h.hex()}"


def verify_password(p, stored):
    try:
        s, h = stored.split(':')
        t = hashlib.pbkdf2_hmac('sha256', p.encode(), s.encode(), 100000)
        return hmac.compare_digest(h, t.hex())
    except:
        return False


def fm(n):
    try:
        return f"{int(round(n)):,}"
    except:
        return '0'


def attach_format(entry):
    def on_key(e):
        if e.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Tab'):
            return
        v = ''.join(c for c in entry.get().replace(',', '') if c.isdigit())
        f = f"{int(v):,}" if v else ''
        if f != entry.get():
            entry.delete(0, tk.END)
            entry.insert(0, f)
    entry.bind('<KeyRelease>', on_key)


def mk_btn(parent, text, cmd, color=C['primary'], icon=''):
    label = f'{icon}  {text}' if icon else text
    return tk.Button(parent, text=label, command=cmd, bg=color, fg='white',
                     font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor='hand2',
                     padx=20, pady=10, activebackground=color, activeforeground='white',
                     bd=0, highlightthickness=0)


def mk_entry(parent, show=None, width=30, justify='right'):
    return tk.Entry(parent, font=('Segoe UI', 11), width=width, show=show,
                    relief=tk.FLAT, bd=0, bg='#FAFBFC', highlightthickness=1,
                    highlightbackground=C['border'], highlightcolor=C['primary'],
                    justify=justify, insertbackground=C['primary'])


def mk_label(parent, text, size=11, bold=False, color=None):
    return tk.Label(parent, text=text,
                    font=('Segoe UI', size, 'bold' if bold else 'normal'),
                    bg=parent.cget('bg'), fg=color or C['text'])


def card(parent, **kw):
    return tk.Frame(parent, bg='white', highlightbackground=C['border'],
                    highlightthickness=1, **kw)


class App:
    def __init__(self, root):
        self.root = root
        root.title('💳 حسابداری حرفه‌ای')
        root.geometry('1150x750')
        root.configure(bg=C['bg'])
        root.minsize(950, 600)
        self.user = None
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ======================================
    #   ورود / ثبت‌نام
    # ======================================
    def show_login(self):
        self.clear()
        self.user = None

        wrap = tk.Frame(self.root, bg=C['primary'])
        wrap.pack(fill=tk.BOTH, expand=True)

        box = card(wrap)
        box.place(relx=0.5, rely=0.5, anchor='center', width=430)

        icon = tk.Canvas(box, width=70, height=55, bg='white', highlightthickness=0)
        icon.pack(pady=(15, 5))
        icon.create_rectangle(5, 5, 65, 50, fill='#6C63FF', outline='#5A52D5', width=2)
        icon.create_rectangle(5, 15, 65, 25, fill='#FDCB6E', outline='')
        icon.create_rectangle(12, 32, 25, 42, fill='#FDCB6E', outline='')
        icon.create_line(35, 35, 55, 35, fill='white', width=2)
        icon.create_line(35, 42, 50, 42, fill='white', width=2)

        tk.Label(box, text='حسابداری حرفه‌ای', font=('Segoe UI', 18, 'bold'),
                 bg='white', fg=C['primary']).pack()
        tk.Label(box, text='سیستم مدیریت مالی', font=('Segoe UI', 10),
                 bg='white', fg=C['text_light']).pack(pady=(2, 15))

        tabs = tk.Frame(box, bg='#F0F0F5', height=38)
        tabs.pack(fill=tk.X, padx=25, pady=(0, 12))
        tabs.pack_propagate(False)

        self.b_l = tk.Button(tabs, text='ورود', font=('Segoe UI', 10, 'bold'),
                             command=lambda: self.tab('login'), relief=tk.FLAT,
                             bg=C['primary'], fg='white', cursor='hand2', bd=0)
        self.b_l.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.b_r = tk.Button(tabs, text='ثبت‌نام', font=('Segoe UI', 10, 'bold'),
                             command=lambda: self.tab('reg'), relief=tk.FLAT,
                             bg='#F0F0F5', fg='#666', cursor='hand2', bd=0)
        self.b_r.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.tc = tk.Frame(box, bg='white')
        self.tc.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 15))

        self.f_login = tk.Frame(self.tc, bg='white')
        self.f_reg = tk.Frame(self.tc, bg='white')
        self._build_login()
        self._build_reg()
        self.f_login.pack(fill=tk.BOTH, expand=True)

    def tab(self, t):
        if t == 'login':
            self.b_l.config(bg=C['primary'], fg='white')
            self.b_r.config(bg='#F0F0F5', fg='#666')
            self.f_reg.pack_forget()
            self.f_login.pack(fill=tk.BOTH, expand=True)
        else:
            self.b_l.config(bg='#F0F0F5', fg='#666')
            self.b_r.config(bg=C['primary'], fg='white')
            self.f_login.pack_forget()
            self.f_reg.pack(fill=tk.BOTH, expand=True)

    def _build_login(self):
        f = self.f_login
        mk_label(f, 'نام کاربری', 10, True).pack(anchor='e', pady=(8, 3))
        self.lu = mk_entry(f)
        self.lu.pack(fill=tk.X, ipady=7)

        mk_label(f, 'رمز عبور', 10, True).pack(anchor='e', pady=(10, 3))
        self.lp = mk_entry(f, show='●')
        self.lp.pack(fill=tk.X, ipady=7)

        self.lm = tk.Label(f, text='', font=('Segoe UI', 9), bg='white', fg=C['danger'])
        self.lm.pack(pady=(8, 0))

        mk_btn(f, 'ورود به سیستم', self.do_login, C['success']).pack(fill=tk.X, pady=(12, 10))

    def _build_reg(self):
        f = self.f_reg

        btn_frame = tk.Frame(f, bg='white')
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        mk_btn(btn_frame, '✅  ایجاد حساب', self.do_reg,
               C['success']).pack(fill=tk.X, ipady=3)

        self.rm = tk.Label(f, text='', font=('Segoe UI', 9), bg='white', fg=C['danger'])
        self.rm.pack(side=tk.BOTTOM, pady=(4, 0))

        for lbl, attr, s in [('نام کاربری *', 'ru', None),
                              ('ایمیل *', 're', None),
                              ('رمز عبور *', 'rp', '●'),
                              ('تکرار رمز *', 'rc', '●'),
                              ('نام کامل', 'rf', None)]:
            mk_label(f, lbl, 10, True).pack(anchor='e', pady=(4, 2))
            e = mk_entry(f, show=s)
            e.pack(fill=tk.X, ipady=5)
            setattr(self, attr, e)

    def msg(self, w, t, c=None):
        w.config(text=t, fg=c or C['danger'])
        w.after(4000, lambda: w.config(text=''))

    def do_login(self):
        u, p = self.lu.get().strip(), self.lp.get()
        if not u or not p:
            return self.msg(self.lm, 'فیلدها را پر کنید.')
        user = next((x for x in data['users'] if x['username'] == u), None)
        if not user or not verify_password(p, user['password_hash']):
            return self.msg(self.lm, 'نام کاربری یا رمز اشتباه است.')
        self.user = user
        self.dashboard()

    def do_reg(self):
        u = self.ru.get().strip()
        e = self.re.get().strip()
        p = self.rp.get()
        c = self.rc.get()
        n = self.rf.get().strip()

        if not u or not e or not p:
            return self.msg(self.rm, 'فیلدهای ضروری را پر کنید.')
        if len(u) < 3:
            return self.msg(self.rm, 'نام کاربری حداقل ۳ کاراکتر')
        if len(p) < 6:
            return self.msg(self.rm, 'رمز حداقل ۶ کاراکتر')
        if p != c:
            return self.msg(self.rm, 'رمزها مطابقت ندارند')
        if any(x['username'] == u or x['email'] == e for x in data['users']):
            return self.msg(self.rm, 'نام کاربری یا ایمیل تکراری است')

        user = {'id': data['nextUserId'], 'username': u, 'email': e,
                'password_hash': hash_password(p), 'full_name': n,
                'phone': '', 'created_at': datetime.now().isoformat()}
        data['nextUserId'] += 1
        data['users'].append(user)
        save()
        messagebox.showinfo('موفقیت', 'ثبت‌نام انجام شد!')
        self.user = user
        self.dashboard()

    # ======================================
    #   داشبورد
    # ======================================
    def dashboard(self):
        self.clear()

        sb = tk.Frame(self.root, bg=C['primary'], width=200)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        sb.pack_propagate(False)

        tk.Label(sb, text='💳', font=('Segoe UI Emoji', 32), bg=C['primary'],
                 fg='white').pack(pady=(20, 3))
        nm = self.user.get('full_name') or self.user['username']
        tk.Label(sb, text=nm, font=('Segoe UI', 11, 'bold'), bg=C['primary'],
                 fg='white').pack(pady=(0, 20))

        items = [('🏠', 'داشبورد', self.p_home),
                 ('💰', 'حساب‌ها', self.p_acc),
                 ('📊', 'تراکنش‌ها', self.p_tx),
                 ('➕', 'تراکنش جدید', self.p_add),
                 ('🤖', 'هوش مصنوعی', self.p_ai),
                 ('⚙️', 'تنظیمات', self.p_settings)]

        self.menu_btns = []
        for ic, txt, cb in items:
            b = tk.Button(sb, text=f'{ic}  {txt}', font=('Segoe UI', 10),
                          bg=C['primary'], fg='white', anchor='e', relief=tk.FLAT,
                          cursor='hand2', pady=10, padx=12,
                          activebackground=C['primary_dark'], activeforeground='white',
                          bd=0, command=lambda c=cb: self.menu(c))
            b.pack(fill=tk.X, padx=6, pady=1)
            self.menu_btns.append((b, cb))

        tk.Frame(sb, bg=C['primary']).pack(fill=tk.BOTH, expand=True)
        mk_btn(sb, 'خروج', self.logout, C['danger'], '🚪').pack(fill=tk.X, padx=15, pady=15)

        self.mf = tk.Frame(self.root, bg=C['bg'])
        self.mf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.p_home()

    def menu(self, cb):
        for b, c in self.menu_btns:
            b.config(bg=C['primary_dark'] if c == cb else C['primary'])
        cb()

    def clr(self):
        for w in self.mf.winfo_children():
            w.destroy()

    def hdr(self, title):
        h = tk.Frame(self.mf, bg=C['bg'])
        h.pack(fill=tk.X, padx=20, pady=(18, 8))
        tk.Label(h, text=title, font=('Segoe UI', 18, 'bold'),
                 bg=C['bg'], fg=C['primary']).pack(side=tk.RIGHT)

    def logout(self):
        if messagebox.askyesno('خروج', 'خارج می‌شوید؟'):
            self.user = None
            self.show_login()

    # ======================================
    #   داشبورد
    # ======================================
    def p_home(self):
        self.clr()
        self.hdr('🏠 داشبورد')
        s = self.summary()

        cf = tk.Frame(self.mf, bg=C['bg'])
        cf.pack(fill=tk.X, padx=20, pady=8)
        cards_data = [
            ('💰 موجودی کل', fm(s['bal']) + ' ریال', C['info']),
            ('📈 درآمد', fm(s['inc']) + ' ریال', C['success']),
            ('📉 هزینه', fm(s['exp']) + ' ریال', C['danger']),
            ('📊 سود خالص', fm(s['net']) + ' ریال', C['warning']),
        ]
        for i, (t, v, c) in enumerate(cards_data):
            crd = card(cf, padx=14, pady=14)
            crd.grid(row=0, column=i, padx=5, sticky='nsew')
            cf.grid_columnconfigure(i, weight=1)
            tk.Label(crd, text=t, font=('Segoe UI', 9), bg='white',
                     fg=C['text_light']).pack(anchor='e')
            tk.Label(crd, text=v, font=('Segoe UI', 13, 'bold'), bg='white',
                     fg=c).pack(anchor='e', pady=(4, 0))

        tk.Label(self.mf, text='📋 آخرین تراکنش‌ها', font=('Segoe UI', 12, 'bold'),
                 bg=C['bg'], fg=C['text']).pack(anchor='e', padx=20, pady=(14, 6))
        self.tx_table(self.mf, limit=10, delete=False)

    # ======================================
    #   حساب‌ها
    # ======================================
    def p_acc(self):
        self.clr()
        self.hdr('💰 مدیریت حساب‌ها')

        tb = tk.Frame(self.mf, bg=C['bg'])
        tb.pack(fill=tk.X, padx=20, pady=5)
        mk_btn(tb, 'افزودن حساب', self.dlg_acc, C['success'], '➕').pack(side=tk.RIGHT)

        accs = [a for a in data['accounts'] if a['user_id'] == self.user['id']]
        if not accs:
            self.empty('هیچ حسابی ثبت نشده')
            return

        self._style()
        cols = ('name', 'type', 'balance', 'currency')
        t = ttk.Treeview(self.mf, columns=cols, show='headings',
                         style='CV.Treeview', height=15)
        for k, txt, w in [('name', 'نام', 260), ('type', 'نوع', 130),
                          ('balance', 'موجودی (ریال)', 200), ('currency', 'ارز', 80)]:
            t.heading(k, text=txt)
            t.column(k, anchor='e' if k in ('name', 'balance') else 'center', width=w)

        for a in accs:
            t.insert('', 'end', values=(a['account_name'], a['account_type'],
                                        fm(a['balance']), a['currency']))
        self._pack_tree(t)

    def dlg_acc(self):
        d = tk.Toplevel(self.root)
        d.title('حساب جدید')
        d.geometry('380x420')
        d.configure(bg='white')
        d.transient(self.root)
        d.grab_set()

        tk.Label(d, text='➕ حساب جدید', font=('Segoe UI', 14, 'bold'),
                 bg='white', fg=C['primary']).pack(pady=15)

        f = tk.Frame(d, bg='white')
        f.pack(fill=tk.BOTH, expand=True, padx=25)

        mk_label(f, 'نام حساب', 10, True).pack(anchor='e', pady=(5, 2))
        ne = mk_entry(f)
        ne.pack(fill=tk.X, ipady=6)

        mk_label(f, 'نوع', 10, True).pack(anchor='e', pady=(10, 2))
        tc = ttk.Combobox(f, values=['نقدی', 'بانکی', 'اعتباری', 'سایر'],
                          state='readonly', font=('Segoe UI', 10))
        tc.current(0)
        tc.pack(fill=tk.X, ipady=4)

        mk_label(f, 'موجودی اولیه', 10, True).pack(anchor='e', pady=(10, 2))
        be = mk_entry(f)
        be.insert(0, '0')
        be.pack(fill=tk.X, ipady=6)
        attach_format(be)

        mk_label(f, 'ارز', 10, True).pack(anchor='e', pady=(10, 2))
        cc = ttk.Combobox(f, values=['IRR', 'USD', 'EUR'], state='readonly',
                          font=('Segoe UI', 10))
        cc.current(0)
        cc.pack(fill=tk.X, ipady=4)

        def save_acc():
            n = ne.get().strip()
            if not n:
                return messagebox.showwarning('خطا', 'نام را وارد کنید', parent=d)
            try:
                b = float(be.get().replace(',', '') or 0)
            except:
                return messagebox.showerror('خطا', 'مبلغ نامعتبر', parent=d)
            data['accounts'].append({
                'id': data['nextAccountId'], 'user_id': self.user['id'],
                'account_name': n, 'account_type': tc.get(),
                'balance': b, 'currency': cc.get()})
            data['nextAccountId'] += 1
            save()
            d.destroy()
            self.p_acc()

        mk_btn(f, 'ذخیره', save_acc, C['success']).pack(fill=tk.X, pady=18)

    # ======================================
    #   تراکنش‌ها
    # ======================================
    def p_tx(self):
        self.clr()
        self.hdr('📊 لیست تراکنش‌ها')

        tb = tk.Frame(self.mf, bg=C['bg'])
        tb.pack(fill=tk.X, padx=20, pady=5)
        mk_btn(tb, 'بازخوانی', self.p_tx, C['info'], '🔄').pack(side=tk.RIGHT)
        mk_btn(tb, 'حذف انتخاب', self.del_tx, C['danger'], '🗑️').pack(side=tk.RIGHT, padx=5)

        self.tx_table(self.mf, limit=500, delete=True)

    def tx_table(self, parent, limit=100, delete=False):
        txs = sorted([t for t in data['transactions'] if t['user_id'] == self.user['id']],
                     key=lambda x: (x['transaction_date'], x['id']), reverse=True)[:limit]
        if not txs:
            self.empty('هیچ تراکنشی یافت نشد')
            return

        self._style()
        cols = ('id', 'date', 'acc', 'name', 'amount', 'type', 'cat')
        t = ttk.Treeview(parent, columns=cols, show='headings',
                         style='CV.Treeview', height=15)
        heads = [('id', 'ID', 45), ('date', 'تاریخ', 100), ('acc', 'حساب', 130),
                 ('name', 'نام', 200), ('amount', 'مبلغ (ریال)', 150),
                 ('type', 'نوع', 70), ('cat', 'دسته', 100)]
        for k, txt, w in heads:
            t.heading(k, text=txt)
            t.column(k, anchor='e' if k in ('acc', 'name', 'amount') else 'center', width=w)

        t.tag_configure('inc', foreground=C['success'])
        t.tag_configure('exp', foreground=C['danger'])

        for x in txs:
            acc = next((a for a in data['accounts'] if a['id'] == x['account_id']), None)
            an = acc['account_name'] if acc else '?'
            nm = (x.get('description') or '').split(' - ')[0] or '-'
            tp = 'درآمد' if x['transaction_type'] == 'income' else 'هزینه'
            tag = 'inc' if x['transaction_type'] == 'income' else 'exp'
            t.insert('', 'end', iid=str(x['id']), tags=(tag,),
                     values=(x['id'], x['transaction_date'], an, nm,
                             fm(x['amount']), tp, x.get('category') or '-'))
        if delete:
            self.tx_tree = t
        self._pack_tree(t)

    def del_tx(self):
        if not hasattr(self, 'tx_tree') or not self.tx_tree:
            return messagebox.showwarning('خطا', 'جدولی نیست')
        s = self.tx_tree.selection()
        if not s:
            return messagebox.showwarning('خطا', 'یک تراکنش انتخاب کنید')
        tid = int(s[0])
        if not messagebox.askyesno('تأیید', 'حذف شود؟'):
            return
        i = next((i for i, t in enumerate(data['transactions'])
                  if t['id'] == tid and t['user_id'] == self.user['id']), None)
        if i is None:
            return
        tx = data['transactions'].pop(i)
        a = next((x for x in data['accounts'] if x['id'] == tx['account_id']), None)
        if a:
            if tx['transaction_type'] == 'income':
                a['balance'] -= tx['amount']
            else:
                a['balance'] += tx['amount']
        save()
        self.p_tx()

    # ======================================
    #   تراکنش جدید
    # ======================================
    def p_add(self):
        self.clr()
        self.hdr('➕ ثبت تراکنش جدید')

        accs = [a for a in data['accounts'] if a['user_id'] == self.user['id']]
        if not accs:
            self.empty('ابتدا یک حساب بسازید')
            return

        bt = tk.Frame(self.mf, bg=C['bg'])
        bt.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=12)
        mk_btn(bt, 'ثبت تراکنش', self.submit_tx, C['success'], '✅').pack(fill=tk.X, ipady=3)

        f = card(self.mf, padx=20, pady=15)
        f.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        mk_label(f, 'نام تراکنش', 10, True).pack(anchor='e', pady=(4, 2))
        self.tn = mk_entry(f, width=45)
        self.tn.insert(0, f"تراکنش {datetime.now().strftime('%H:%M')}")
        self.tn.pack(anchor='e', ipady=5)

        mk_label(f, 'حساب', 10, True).pack(anchor='e', pady=(8, 2))
        self.ta = ttk.Combobox(f, state='readonly', width=43, font=('Segoe UI', 10))
        self.ta['values'] = [f"{a['account_name']} (موجودی: {fm(a['balance'])})" for a in accs]
        self.ta.current(0)
        self.ta.pack(anchor='e', ipady=4)
        self.ta_list = accs

        mk_label(f, 'نوع تراکنش', 10, True).pack(anchor='e', pady=(8, 2))
        self.tt = tk.StringVar(value='income')
        tf = tk.Frame(f, bg='white')
        tf.pack(anchor='e')
        for txt, val in [('هزینه', 'expense'), ('درآمد', 'income')]:
            tk.Radiobutton(tf, text=txt, variable=self.tt, value=val, bg='white',
                           font=('Segoe UI', 10), activebackground='white',
                           cursor='hand2').pack(side=tk.RIGHT, padx=6)

        mk_label(f, 'مبلغ (ریال)', 10, True).pack(anchor='e', pady=(8, 2))
        self.tam = mk_entry(f, width=45)
        self.tam.pack(anchor='e', ipady=5)
        attach_format(self.tam)

        mk_label(f, 'دسته‌بندی', 10, True).pack(anchor='e', pady=(8, 2))
        self.tc = ttk.Combobox(f, state='readonly', width=43, font=('Segoe UI', 10),
                                values=['غذا', 'حمل و نقل', 'قبض', 'تفریح', 'خرید',
                                        'درمان', 'آموزش', 'سرمایه‌گذاری', 'سایر'])
        self.tc.current(0)
        self.tc.pack(anchor='e', ipady=4)

        mk_label(f, 'تاریخ', 10, True).pack(anchor='e', pady=(8, 2))
        self.td = mk_entry(f, width=45)
        self.td.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.td.pack(anchor='e', ipady=5)

        mk_label(f, 'توضیحات', 10, True).pack(anchor='e', pady=(8, 2))
        self.tx = mk_entry(f, width=45)
        self.tx.pack(anchor='e', ipady=5)

    def submit_tx(self):
        try:
            i = self.ta.current()
            a = self.ta_list[i]
            am = float(self.tam.get().replace(',', ''))
            if am <= 0:
                raise ValueError
        except:
            return messagebox.showerror('خطا', 'حساب و مبلغ معتبر وارد کنید')

        nm = self.tn.get().strip() or '-'
        ds = self.tx.get().strip()
        desc = nm + (f' - {ds}' if ds else '')

        tx = {'id': data['nextTxId'], 'user_id': self.user['id'],
              'account_id': a['id'], 'amount': am, 'transaction_type': self.tt.get(),
              'category': self.tc.get(), 'description': desc,
              'transaction_date': self.td.get()}
        data['nextTxId'] += 1
        data['transactions'].append(tx)

        if tx['transaction_type'] == 'income':
            a['balance'] += am
        else:
            a['balance'] -= am

        save()
        messagebox.showinfo('موفقیت', 'ثبت شد!')
        self.p_home()

    # ======================================
    #   هوش مصنوعی
    # ======================================
    def p_ai(self):
        self.clr()
        self.hdr('🤖 هوش مصنوعی')

        tb = tk.Frame(self.mf, bg='#F0F0F5', height=38)
        tb.pack(fill=tk.X, padx=20, pady=(0, 10))
        tb.pack_propagate(False)

        self.ai_t = tk.StringVar(value='an')
        self.bt_an = tk.Button(tb, text='🧠 تحلیل اقتصادی', font=('Segoe UI', 10, 'bold'),
                               command=lambda: self.ai_tab('an'), relief=tk.FLAT,
                               bg=C['primary'], fg='white', cursor='hand2', bd=0)
        self.bt_an.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.bt_gen = tk.Button(tb, text='🧪 تولید داده', font=('Segoe UI', 10, 'bold'),
                                command=lambda: self.ai_tab('gen'), relief=tk.FLAT,
                                bg='#F0F0F5', fg='#666', cursor='hand2', bd=0)
        self.bt_gen.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.ai_c = tk.Frame(self.mf, bg=C['bg'])
        self.ai_c.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.ai_render()

    def ai_tab(self, t):
        self.ai_t.set(t)
        if t == 'an':
            self.bt_an.config(bg=C['primary'], fg='white')
            self.bt_gen.config(bg='#F0F0F5', fg='#666')
        else:
            self.bt_an.config(bg='#F0F0F5', fg='#666')
            self.bt_gen.config(bg=C['primary'], fg='white')
        self.ai_render()

    def ai_render(self):
        for w in self.ai_c.winfo_children():
            w.destroy()
        if self.ai_t.get() == 'an':
            self._an_tab()
        else:
            self._gen_tab()

    def _an_tab(self):
        p = self.ai_c
        a = self.analysis()

        sf = tk.Frame(p, bg=a['color'], padx=18, pady=15)
        sf.pack(fill=tk.X, pady=(0, 10))
        tk.Label(sf, text=f"{a['emoji']}  {a['text']}", font=('Segoe UI', 16, 'bold'),
                 bg=a['color'], fg='white').pack(anchor='e')
        tk.Label(sf, text=a['desc'], font=('Segoe UI', 10), bg=a['color'], fg='white',
                 wraplength=700, justify='right').pack(anchor='e', pady=(3, 0))

        gf = tk.Frame(p, bg=C['bg'])
        gf.pack(fill=tk.X, pady=(0, 10))
        stats = [('نسبت هزینه/درآمد', f"{a['ratio']:.1f}%",
                  C['info'] if a['ratio'] < 70 else C['warning']),
                 ('نرخ پس‌انداز', f"{a['save']:.1f}%",
                  C['success'] if a['save'] > 20 else C['danger']),
                 ('پرهزینه‌ترین', a['top'][0], C['danger']),
                 ('مجموع آن', fm(a['top'][1]) + ' ریال', C['danger'])]

        for i, (t, v, c) in enumerate(stats):
            crd = card(gf, padx=12, pady=12)
            crd.grid(row=0, column=i, padx=4, sticky='nsew')
            gf.grid_columnconfigure(i, weight=1)
            tk.Label(crd, text=t, font=('Segoe UI', 9), bg='white',
                     fg=C['text_light']).pack(anchor='e')
            tk.Label(crd, text=v, font=('Segoe UI', 12, 'bold'), bg='white',
                     fg=c).pack(anchor='e', pady=(3, 0))

        row = tk.Frame(p, bg=C['bg'])
        row.pack(fill=tk.BOTH, expand=True)

        cc = card(row, padx=12, pady=12)
        cc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(cc, text='📈 توزیع هزینه‌ها', font=('Segoe UI', 11, 'bold'),
                 bg='white', fg=C['primary']).pack(anchor='e')
        cv = tk.Canvas(cc, bg='white', height=240, highlightthickness=0)
        cv.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        if a['cats']:
            self._pie(cv, a['cats'])

        ac = card(row, padx=12, pady=12)
        ac.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(ac, text='💡 توصیه‌های هوشمند', font=('Segoe UI', 11, 'bold'),
                 bg='white', fg=C['primary']).pack(anchor='e', pady=(0, 6))
        for adv in a['advices']:
            it = tk.Frame(ac, bg='#FAFAFC', padx=10, pady=8)
            it.pack(fill=tk.X, pady=3)
            tk.Label(it, text=adv['icon'], font=('Segoe UI Emoji', 13),
                     bg='#FAFAFC').pack(side=tk.RIGHT, padx=(0, 6))
            tk.Label(it, text=adv['text'], font=('Segoe UI', 9), bg='#FAFAFC',
                     fg=C['text'], wraplength=280, justify='right',
                     anchor='e').pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def analysis(self):
        uid = self.user['id']
        txs = [t for t in data['transactions'] if t['user_id'] == uid]
        accs = [a for a in data['accounts'] if a['user_id'] == uid]

        if not txs:
            return {'emoji': '📭', 'text': 'داده کافی نیست',
                    'desc': 'هنوز تراکنشی ثبت نشده. برای تحلیل، به تب «تولید داده» بروید.',
                    'color': C['text_light'], 'ratio': 0, 'save': 0,
                    'top': ('-', 0), 'cats': [],
                    'advices': [{'icon': '💡', 'text': 'یک حساب بسازید و اولین تراکنش را ثبت کنید.'}]}

        inc = sum(t['amount'] for t in txs if t['transaction_type'] == 'income')
        exp = sum(t['amount'] for t in txs if t['transaction_type'] == 'expense')
        bal = sum(a['balance'] for a in accs)

        ratio = (exp / inc * 100) if inc > 0 else 100
        sv = ((inc - exp) / inc * 100) if inc > 0 else 0

        if inc == 0:
            em, tx, cl = '⚠️', 'بدون درآمد', C['danger']
            ds = 'فقط هزینه دارید! این وضعیت پایدار نیست.'
        elif ratio > 100:
            em, tx, cl = '🚨', 'وضعیت بحرانی', C['danger']
            ds = f'هزینه‌های شما {ratio:.0f}٪ درآمدتان است! بیش از درآمد خرج می‌کنید.'
        elif ratio > 80:
            em, tx, cl = '⚠️', 'وضعیت هشدار', C['warning']
            ds = f'شما {ratio:.0f}٪ درآمدتان را خرج می‌کنید. پس‌انداز کم دارید.'
        elif ratio > 50:
            em, tx, cl = '👍', 'وضعیت متوسط', C['info']
            ds = f'شما {ratio:.0f}٪ درآمدتان را خرج می‌کنید. تعادل دارید.'
        else:
            em, tx, cl = '🌟', 'وضعیت عالی', C['success']
            ds = f'فقط {ratio:.0f}٪ درآمدتان خرج می‌شود! پس‌انداز فوق‌العاده.'

        cat_sum = {}
        for t in txs:
            if t['transaction_type'] == 'expense':
                k = t.get('category') or 'سایر'
                cat_sum[k] = cat_sum.get(k, 0) + t['amount']
        sorted_cats = sorted(cat_sum.items(), key=lambda x: -x[1])
        top = sorted_cats[0] if sorted_cats else ('-', 0)

        adv = []
        if ratio > 100:
            adv.append({'icon': '🚨', 'text': 'هزینه‌ها را فوراً کاهش دهید!'})
        elif ratio > 80:
            adv.append({'icon': '⚠️', 'text': f'هدف: کاهش {ratio-70:.0f}٪ هزینه'})

        if 0 <= sv < 20 and inc > 0:
            target = inc * 0.2
            gap = target - (inc - exp)
            if gap > 0:
                adv.append({'icon': '💰', 'text': f'ماهانه {fm(gap)} ریال بیشتر پس‌انداز کنید'})

        if top[1] > 0 and exp > 0:
            pct = top[1] / exp * 100
            adv.append({'icon': '🎯', 'text': f'بیشترین هزینه در «{top[0]}» ({pct:.0f}٪)'})

        if bal > 0:
            adv.append({'icon': '🏦', 'text': f'موجودی {fm(bal)} ریال — قابل سرمایه‌گذاری'})

        now = datetime.now()
        recent = [t for t in txs if (now - datetime.strptime(t['transaction_date'], '%Y-%m-%d')).days <= 30]
        older = [t for t in txs if 30 < (now - datetime.strptime(t['transaction_date'], '%Y-%m-%d')).days <= 60]
        if recent and older:
            re = sum(t['amount'] for t in recent if t['transaction_type'] == 'expense')
            oe = sum(t['amount'] for t in older if t['transaction_type'] == 'expense')
            if oe > 0:
                d = ((re - oe) / oe) * 100
                if d > 15:
                    adv.append({'icon': '📈', 'text': f'هزینه اخیر {d:.0f}٪ بیشتر شده'})
                elif d < -15:
                    adv.append({'icon': '📉', 'text': f'عالی! {abs(d):.0f}٪ کمتر شده'})

        if not adv:
            adv.append({'icon': '✅', 'text': 'وضعیت مالی متعادل است'})

        return {'emoji': em, 'text': tx, 'desc': ds, 'color': cl,
                'ratio': ratio, 'save': sv, 'top': top,
                'cats': sorted_cats[:6], 'advices': adv[:5]}

    def _pie(self, cv, data):
        cv.delete('all')
        total = sum(v for _, v in data)
        if total == 0:
            return
        cv.update_idletasks()
        w = cv.winfo_width() or 350
        h = cv.winfo_height() or 220
        size = min(w, h) - 30
        cx, cy = w // 2, h // 2
        r = size // 2

        cols = ['#6C63FF', '#FF6584', '#00B894', '#FDCB6E', '#74B9FF', '#FF6B6B', '#A29BFE']
        start = 90
        for i, (_, v) in enumerate(data):
            ext = -(v / total * 360)
            cv.create_arc(cx - r, cy - r, cx + r, cy + r, start=start, extent=ext,
                          fill=cols[i % len(cols)], outline='white', width=2)
            start += ext

        inner = int(r * 0.55)
        cv.create_oval(cx - inner, cy - inner, cx + inner, cy + inner,
                       fill='white', outline='white')
        cv.create_text(cx, cy - 6, text='کل هزینه',
                       font=('Segoe UI', 8), fill=C['text_light'])
        cv.create_text(cx, cy + 8, text=fm(total),
                       font=('Segoe UI', 10, 'bold'), fill=C['text'])

        lx, ly = 8, 8
        for i, (cat, v) in enumerate(data):
            cv.create_rectangle(lx, ly + i * 18, lx + 10, ly + i * 18 + 10,
                                fill=cols[i % len(cols)], outline='')
            cv.create_text(lx + 15, ly + i * 18 + 5,
                           text=f'{cat} ({v/total*100:.0f}٪)',
                           anchor='w', font=('Segoe UI', 8), fill=C['text'])

    def _gen_tab(self):
        p = self.ai_c
        c = card(p, padx=30, pady=25)
        c.pack(fill=tk.BOTH, expand=True)

        tk.Label(c, text='🧪', font=('Segoe UI Emoji', 42), bg='white').pack(pady=(5, 0))
        tk.Label(c, text='تولید داده هوشمند', font=('Segoe UI', 16, 'bold'),
                 bg='white', fg=C['primary']).pack()
        tk.Label(c, text='داده‌های تصادفی برای تست', font=('Segoe UI', 10),
                 bg='white', fg=C['text_light']).pack(pady=(2, 20))

        tk.Label(c, text='تعداد تراکنش:', font=('Segoe UI', 10, 'bold'),
                 bg='white', fg=C['text']).pack(anchor='e')

        rw = tk.Frame(c, bg='white')
        rw.pack(fill=tk.X, pady=(5, 15))

        self.ai_n = tk.Entry(rw, font=('Segoe UI', 12), width=12, relief=tk.FLAT,
                             bd=0, bg='#FAFBFC', highlightthickness=1,
                             highlightbackground=C['border'], highlightcolor=C['primary'],
                             justify='center')
        self.ai_n.insert(0, '100')
        self.ai_n.pack(side=tk.RIGHT, ipady=8, ipadx=8)

        for lbl, v in [('کم', '50'), ('متوسط', '100'), ('زیاد', '500')]:
            tk.Button(rw, text=lbl, font=('Segoe UI', 9), bg='#F0F0F5',
                      fg=C['text'], relief=tk.FLAT, cursor='hand2', padx=12,
                      pady=6, bd=0, command=lambda x=v: self._set_n(x)
                      ).pack(side=tk.RIGHT, padx=3)

        info = tk.Frame(c, bg='#F5F5FF', padx=12, pady=10,
                        highlightbackground='#E0E0FF', highlightthickness=1)
        info.pack(fill=tk.X, pady=(0, 15))
        tk.Label(info, text='ℹ️  مبالغ بین ۱۰۰,۰۰۰ تا ۵,۰۰۰,۰۰۰ ریال در ۶ ماه اخیر',
                 font=('Segoe UI', 9), bg='#F5F5FF', fg=C['text']).pack(anchor='e')

        mk_btn(c, 'شروع تولید', self.gen_data, C['success'], '🚀').pack(fill=tk.X, ipady=8)

    def _set_n(self, v):
        self.ai_n.delete(0, tk.END)
        self.ai_n.insert(0, v)

    def gen_data(self):
        try:
            n = min(int(self.ai_n.get()), 500)
            if n <= 0:
                raise ValueError
        except:
            return messagebox.showerror('خطا', 'عدد معتبر وارد کنید')

        accs = [a for a in data['accounts'] if a['user_id'] == self.user['id']]
        if not accs:
            return messagebox.showwarning('خطا', 'ابتدا حساب بسازید')
        a = accs[0]

        cats = ['غذا', 'حمل و نقل', 'قبض', 'تفریح', 'خرید', 'درمان', 'آموزش', 'سرمایه‌گذاری']
        for i in range(n):
            am = random.randint(100000, 5000000)
            tp = random.choice(['income', 'expense'])
            ct = random.choice(cats)
            d = (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
            data['transactions'].append({
                'id': data['nextTxId'], 'user_id': self.user['id'],
                'account_id': a['id'], 'amount': am, 'transaction_type': tp,
                'category': ct, 'description': f'تراکنش خودکار {i+1}',
                'transaction_date': d})
            data['nextTxId'] += 1
            if tp == 'income':
                a['balance'] += am
            else:
                a['balance'] -= am
        save()
        messagebox.showinfo('موفقیت', f'{n} تراکنش تولید شد!')
        self.p_home()

    # ======================================
    #   تنظیمات (جدید)
    # ======================================
    def p_settings(self):
        self.clr()
        self.hdr('⚙️ تنظیمات')

        info_card = card(self.mf, padx=20, pady=15)
        info_card.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(info_card, text='👤 اطلاعات کاربر',
                 font=('Segoe UI', 12, 'bold'), bg='white',
                 fg=C['primary']).pack(anchor='e', pady=(0, 10))

        rows = [
            ('نام کاربری', self.user['username']),
            ('ایمیل', self.user.get('email', '-')),
            ('نام کامل', self.user.get('full_name') or 'ثبت نشده'),
            ('تاریخ عضویت', (self.user.get('created_at', '-') or '-')[:10]),
        ]
        for lbl, val in rows:
            r = tk.Frame(info_card, bg='white')
            r.pack(fill=tk.X, pady=3)
            tk.Label(r, text=lbl, font=('Segoe UI', 10),
                     bg='white', fg=C['text_light']).pack(side=tk.RIGHT, padx=(0, 10))
            tk.Label(r, text=val, font=('Segoe UI', 10, 'bold'),
                     bg='white', fg=C['text']).pack(side=tk.RIGHT)

        stats_card = card(self.mf, padx=20, pady=15)
        stats_card.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(stats_card, text='📊 آمار داده‌های شما',
                 font=('Segoe UI', 12, 'bold'), bg='white',
                 fg=C['primary']).pack(anchor='e', pady=(0, 10))

        my_accs = [a for a in data['accounts'] if a['user_id'] == self.user['id']]
        my_txs = [t for t in data['transactions'] if t['user_id'] == self.user['id']]
        file_size = os.path.getsize(DATA_FILE) // 1024 if os.path.exists(DATA_FILE) else 0

        stats = [
            ('تعداد حساب‌ها', f"{len(my_accs)}"),
            ('تعداد تراکنش‌ها', f"{len(my_txs)}"),
            ('حجم فایل داده', f"{file_size} KB"),
        ]
        for lbl, val in stats:
            r = tk.Frame(stats_card, bg='white')
            r.pack(fill=tk.X, pady=3)
            tk.Label(r, text=lbl, font=('Segoe UI', 10),
                     bg='white', fg=C['text_light']).pack(side=tk.RIGHT, padx=(0, 10))
            tk.Label(r, text=val, font=('Segoe UI', 10, 'bold'),
                     bg='white', fg=C['info']).pack(side=tk.RIGHT)

        danger = tk.Frame(self.mf, bg='#FFF5F5', padx=20, pady=15,
                          highlightbackground='#FFD0D0', highlightthickness=1)
        danger.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(danger, text='⚠️ منطقه خطرناک',
                 font=('Segoe UI', 12, 'bold'), bg='#FFF5F5',
                 fg=C['danger']).pack(anchor='e')
        tk.Label(danger, text='این عملیات غیرقابل بازگشت است! قبل از ادامه مطمئن شوید.',
                 font=('Segoe UI', 9), bg='#FFF5F5',
                 fg=C['text_light']).pack(anchor='e', pady=(2, 12))

        mk_btn(danger, '🗑️  ریست کل داده‌ها', self.reset_data,
               C['danger']).pack(fill=tk.X, ipady=4)

    def reset_data(self):
        my_accs = [a for a in data['accounts'] if a['user_id'] == self.user['id']]
        my_txs = [t for t in data['transactions'] if t['user_id'] == self.user['id']]

        msg = (f"آیا مطمئن هستید؟\n\n"
               f"🗑️ {len(my_accs)} حساب\n"
               f"🗑️ {len(my_txs)} تراکنش\n\n"
               f"همه این داده‌ها برای همیشه حذف می‌شوند.\n"
               f"حساب کاربری شما باقی می‌ماند.")

        if not messagebox.askyesno('⚠️ تأیید ریست', msg):
            return
        if not messagebox.askyesno('🚨 تأیید نهایی', 'آخرین هشدار!\nمطمئن هستید؟'):
            return

        uid = self.user['id']
        data['accounts'] = [a for a in data['accounts'] if a['user_id'] != uid]
        data['transactions'] = [t for t in data['transactions'] if t['user_id'] != uid]
        save()
        messagebox.showinfo('موفقیت', '✅ همه داده‌های شما پاک شد!')
        self.p_settings()

    # ======================================
    #   کمکی‌ها
    # ======================================
    def summary(self, days=30):
        since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        txs = [t for t in data['transactions']
               if t['user_id'] == self.user['id'] and t['transaction_date'] >= since]
        accs = [a for a in data['accounts'] if a['user_id'] == self.user['id']]
        inc = sum(t['amount'] for t in txs if t['transaction_type'] == 'income')
        exp = sum(t['amount'] for t in txs if t['transaction_type'] == 'expense')
        bal = sum(a['balance'] for a in accs)
        return {'inc': inc, 'exp': exp, 'bal': bal, 'net': inc - exp}

    def empty(self, text):
        tk.Label(self.mf, text=text, font=('Segoe UI', 12), bg=C['bg'],
                 fg=C['text_light']).pack(pady=50)

    def _style(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('CV.Treeview', background='white', foreground=C['text'],
                    rowheight=30, fieldbackground='white', borderwidth=0,
                    font=('Segoe UI', 10))
        s.configure('CV.Treeview.Heading', background=C['primary'], foreground='white',
                    font=('Segoe UI', 10, 'bold'), borderwidth=0)

    def _pack_tree(self, tree):
        fr = tk.Frame(self.mf, bg='white')
        fr.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        sb = ttk.Scrollbar(fr, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()