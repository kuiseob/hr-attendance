#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO JIN PRECISION 인사/근태 관리 시스템 (HR & Attendance).

구성:
  1. Employee_Master (인사 기본정보)
  2. Attendance_Log (근태관리)
  3. Leave_Management (휴가관리)
  4. Payroll (급여 기초)
  5. Dashboard (요약)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, os, sys
from datetime import datetime, date, timedelta

COMPANY = "SEO JIN PRECISION CO."

# ────────────────────────────────────────
# 색상 테마
# ────────────────────────────────────────
C = {
    'primary':      '#1565C0',  # 파랑 (HR 테마)
    'primary_dark': '#0D47A1',
    'accent':       '#FF6F00',
    'header_bg':    '#1565C0',
    'sidebar_bg':   '#ECEFF1',
    'bg':           '#F5F7FA',
    'border':       '#CFD8DC',
    'text':         '#263238',
    'secondary':    '#546E7A',
    'success':      '#2E7D32',
    'warning':      '#E65100',
    'danger':       '#C62828',
    'urgent_bg':    '#FFEBEE',
}

# ────────────────────────────────────────
# DB
# ────────────────────────────────────────
class DB:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(base, "hr.db")
        print(f"[DB] {self.path}")
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create()
        self._seed()

    def _create(self):
        c = self.conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            dept TEXT DEFAULT '',
            position TEXT DEFAULT '',
            join_date TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            base_salary REAL DEFAULT 0,
            status TEXT DEFAULT '재직',
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            work_date TEXT NOT NULL,
            check_in TEXT DEFAULT '',
            check_out TEXT DEFAULT '',
            work_hours REAL DEFAULT 0,
            overtime_hours REAL DEFAULT 0,
            status TEXT DEFAULT '정상',
            memo TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(emp_id) REFERENCES employees(id)
        );
        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            days REAL DEFAULT 0,
            reason TEXT DEFAULT '',
            approval TEXT DEFAULT '대기',
            approver TEXT DEFAULT '',
            memo TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(emp_id) REFERENCES employees(id)
        );
        CREATE TABLE IF NOT EXISTS payrolls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            pay_month TEXT NOT NULL,
            base_salary REAL DEFAULT 0,
            overtime_pay REAL DEFAULT 0,
            bonus REAL DEFAULT 0,
            deduction REAL DEFAULT 0,
            net_pay REAL DEFAULT 0,
            paid_date TEXT DEFAULT '',
            memo TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(emp_id) REFERENCES employees(id)
        );
        """)
        self.conn.commit()

    def _seed(self):
        c = self.conn.cursor()
        if c.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
            samples = [
                ('E2026001', '김철수', '생산팀', '과장', '2020-03-15', '010-1111-2222', 'kim@seojin.kr', 4200000),
                ('E2026002', '이영희', '품질팀', '대리', '2021-07-01', '010-2222-3333', 'lee@seojin.kr', 3500000),
                ('E2026003', '박민수', '경영지원', '부장', '2018-01-10', '010-3333-4444', 'park@seojin.kr', 5500000),
                ('E2026004', '정수진', '생산팀', '사원', '2024-09-20', '010-4444-5555', 'jung@seojin.kr', 2800000),
                ('E2026005', '최동현', '영업팀', '차장', '2019-05-12', '010-5555-6666', 'choi@seojin.kr', 4800000),
            ]
            for s in samples:
                c.execute("""INSERT INTO employees(emp_no,name,dept,position,join_date,phone,email,base_salary)
                             VALUES(?,?,?,?,?,?,?,?)""", s)
        self.conn.commit()

    def query(self, sql, params=()):
        return self.conn.execute(sql, params).fetchall()

    def execute(self, sql, params=()):
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur


# ────────────────────────────────────────
# UI 헬퍼
# ────────────────────────────────────────
def commit_inputs(widget):
    try:
        top = widget.winfo_toplevel()
        top.focus_set()
        top.update_idletasks()
        top.update()
    except Exception: pass

BTN_THEMES = {
    'save':    ('#2E7D32', '#1B5E20'),
    'update':  ('#E65100', '#BF360C'),
    'delete':  ('#C62828', '#8E0000'),
    'action':  ('#1565C0', '#0D47A1'),
    'export':  ('#5E35B1', '#311B92'),
    'neutral': ('#546E7A', '#37474F'),
}

def color_btn(parent, text, cmd, theme='save', size=14, padx=22, pady=10):
    bg, hover = BTN_THEMES.get(theme, BTN_THEMES['save'])
    wrap = tk.Frame(parent, bg=bg, bd=0, highlightthickness=0, cursor='hand2')
    lbl = tk.Label(wrap, text=text, font=('Malgun Gothic', size, 'bold'),
                   bg=bg, fg='white', padx=padx, pady=pady, cursor='hand2')
    lbl.pack(fill='both', expand=True)
    def _click(e=None):
        commit_inputs(wrap); cmd()
    def _enter(e=None):
        wrap.config(bg=hover); lbl.config(bg=hover)
    def _leave(e=None):
        wrap.config(bg=bg); lbl.config(bg=bg)
    for w in (wrap, lbl):
        w.bind('<Button-1>', _click)
        w.bind('<Enter>', _enter)
        w.bind('<Leave>', _leave)
    return wrap

def make_label(parent, text, bold=False, size=10, color=None, **kw):
    return tk.Label(parent, text=text,
                    font=('Malgun Gothic', size, 'bold' if bold else 'normal'),
                    fg=color or C['text'], **kw)

def make_entry(parent, var, width=18, **kw):
    """입력 칸 — 흰색 배경 + 진한 테두리로 명확히 표시."""
    return tk.Entry(parent, textvariable=var,
                    font=('Malgun Gothic', 11),
                    relief='solid', bd=1,
                    bg='white', fg='#212121',
                    highlightthickness=2,
                    highlightbackground='#90A4AE',
                    highlightcolor=C['primary'],
                    insertbackground=C['primary'],
                    width=width, **kw)

def make_combo(parent, var, values, width=18, state='readonly', **kw):
    return ttk.Combobox(parent, textvariable=var, values=values,
                        font=('Malgun Gothic', 11), width=width, state=state, **kw)

def setup_treeview_style():
    style = ttk.Style()
    try: style.theme_use('clam')
    except: pass
    style.configure('PM.Treeview', background='white', fieldbackground='white',
                    foreground=C['text'], rowheight=28, font=('Malgun Gothic', 10))
    style.configure('PM.Treeview.Heading', background=C['primary'],
                    foreground='white', font=('Malgun Gothic', 10, 'bold'),
                    padding=6)
    style.map('PM.Treeview',
              background=[('selected', '#BBDEFB')],
              foreground=[('selected', C['text'])])
    # Combobox 통일 스타일
    style.configure('TCombobox',
                    fieldbackground='white', background='white',
                    foreground='#212121', bordercolor='#90A4AE',
                    arrowcolor=C['primary'], borderwidth=2,
                    relief='solid', padding=4)
    style.map('TCombobox',
              fieldbackground=[('readonly', 'white'), ('focus', 'white')],
              bordercolor=[('focus', C['primary'])],
              lightcolor=[('focus', C['primary'])],
              darkcolor=[('focus', C['primary'])])

def make_tree(parent, cols, widths, height=12):
    tree = ttk.Treeview(parent, columns=cols, show='headings',
                        height=height, style='PM.Treeview')
    for c, w in zip(cols, widths):
        tree.heading(c, text=c); tree.column(c, width=w, anchor='center')
    sy = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=sy.set)
    sy.pack(side='right', fill='y'); tree.pack(side='left', fill='both', expand=True)
    tree.tag_configure('even',     background='#F5F7FA')
    tree.tag_configure('pass_tag', background='#E8F5E9')
    tree.tag_configure('fail_tag', background='#FFEBEE')
    tree.tag_configure('warn_tag', background='#FFF3E0')
    return tree

def fill_tree(tree, rows, tag_fn=None):
    for r in tree.get_children(): tree.delete(r)
    for i, row in enumerate(rows):
        tag = tag_fn(i, row) if tag_fn else ('even' if i%2 else '')
        tree.insert('', 'end', values=tuple(row), tags=(tag,))

def page_header(parent, title, sub=''):
    f = tk.Frame(parent, bg='white', height=58); f.pack(fill='x'); f.pack_propagate(False)
    tk.Label(f, text=title, font=('Malgun Gothic', 18, 'bold'),
             fg=C['primary'], bg='white').pack(side='left', padx=24, pady=12)
    if sub:
        tk.Label(f, text=sub, font=('Malgun Gothic', 10),
                 fg=C['secondary'], bg='white').pack(side='left', pady=18)
    tk.Frame(parent, bg=C['primary'], height=2).pack(fill='x')


# ────────────────────────────────────────
# 메인 앱
# ────────────────────────────────────────
class HRApp:
    def __init__(self):
        self.db = DB()
        setup_treeview_style()
        self.user = {'name': '관리자', 'team': '관리'}
        self.root = tk.Tk()
        self.root.title(f"인사/근태 관리 시스템 - {COMPANY}")
        self.root.geometry("1340x820")
        self.root.configure(bg=C['bg'])
        self.root.minsize(1100, 680)
        self._show_splash()
        self.root.mainloop()

    def _show_splash(self):
        for w in self.root.winfo_children(): w.destroy()
        self.root.geometry("720x520")
        self.root.resizable(False, False)
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
        x = (sw - 720) // 2; y = (sh - 520) // 2
        self.root.geometry(f"720x520+{x}+{y}")

        bg = tk.Frame(self.root, bg=C['primary_dark']); bg.pack(fill='both', expand=True)
        tk.Frame(bg, bg=C['primary_dark'], height=70).pack()
        tk.Label(bg, text="👥", font=('Segoe UI Emoji', 84),
                 fg=C['accent'], bg=C['primary_dark']).pack()
        tk.Label(bg, text="서 진 정 밀", font=('Malgun Gothic', 38, 'bold'),
                 fg='white', bg=C['primary_dark']).pack(pady=(14, 4))
        tk.Label(bg, text=COMPANY, font=('Malgun Gothic', 13),
                 fg='#90CAF9', bg=C['primary_dark']).pack()
        tk.Frame(bg, bg='#90CAF9', height=2, width=320).pack(pady=18)
        tk.Label(bg, text="인사 / 근태 관리 시스템", font=('Malgun Gothic', 18, 'bold'),
                 fg='white', bg=C['primary_dark']).pack()
        tk.Label(bg, text="HR & Attendance Management System",
                 font=('Malgun Gothic', 10), fg='#B0BEC5',
                 bg=C['primary_dark']).pack(pady=(2, 0))
        tk.Label(bg, text="Enter 키를 누르거나 화면을 클릭하세요",
                 font=('Malgun Gothic', 11, 'bold'),
                 fg=C['accent'], bg=C['primary_dark']).pack(pady=(28, 6))
        bot = tk.Frame(bg, bg=C['primary_dark']); bot.pack(side='bottom', fill='x', pady=14)
        tk.Label(bot, text=datetime.now().strftime("%Y-%m-%d  %H:%M"),
                 font=('Malgun Gothic', 9), fg='#78909C',
                 bg=C['primary_dark']).pack()
        def _enter(e=None):
            self.root.unbind('<Return>'); self.root.unbind('<KP_Enter>')
            self.root.unbind('<Button-1>')
            self._show_main()
        self.root.bind('<Return>', _enter)
        self.root.bind('<KP_Enter>', _enter)
        self.root.bind('<Button-1>', _enter)
        self.root.focus_force()

    def _show_main(self):
        for w in self.root.winfo_children(): w.destroy()
        self.root.geometry("1340x820")
        self.root.resizable(True, True)

        self._build_header()
        content = tk.Frame(self.root, bg=C['bg']); content.pack(fill='both', expand=True)
        self._build_sidebar(content)

        # 페이지 영역 (스크롤)
        scroll_wrap = tk.Frame(content, bg=C['bg'])
        scroll_wrap.pack(side='left', fill='both', expand=True)
        vbar = ttk.Scrollbar(scroll_wrap, orient='vertical')
        hbar = ttk.Scrollbar(scroll_wrap, orient='horizontal')
        canvas = tk.Canvas(scroll_wrap, bg=C['bg'], highlightthickness=0,
                           yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        vbar.config(command=canvas.yview); hbar.config(command=canvas.xview)
        vbar.pack(side='right', fill='y'); hbar.pack(side='bottom', fill='x')
        canvas.pack(side='left', fill='both', expand=True)

        self.page_area = tk.Frame(canvas, bg=C['bg'])
        self._page_window = canvas.create_window((0, 0), window=self.page_area, anchor='nw')
        self._page_canvas = canvas

        def _on_inner(e): canvas.configure(scrollregion=canvas.bbox('all'))
        def _on_canvas(e):
            iw = self.page_area.winfo_reqwidth()
            canvas.itemconfig(self._page_window, width=max(e.width, iw))
        self.page_area.bind('<Configure>', _on_inner)
        canvas.bind('<Configure>', _on_canvas)
        def _on_wheel(e):
            d = -int(e.delta) if sys.platform == 'darwin' else -int(e.delta/120)
            canvas.yview_scroll(d, 'units')
        canvas.bind_all('<MouseWheel>', _on_wheel)
        canvas.bind_all('<Button-4>', lambda e: canvas.yview_scroll(-1, 'units'))
        canvas.bind_all('<Button-5>', lambda e: canvas.yview_scroll(1, 'units'))

        self._nav('dashboard')

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=C['header_bg'], height=56); hdr.pack(fill='x'); hdr.pack_propagate(False)
        tk.Label(hdr, text=f"  {COMPANY}  |  인사/근태 관리 시스템",
                 font=('Malgun Gothic', 14, 'bold'),
                 fg='white', bg=C['header_bg']).pack(side='left', padx=10)
        tk.Label(hdr, text=f"{self.user['name']}  ({self.user['team']})",
                 font=('Malgun Gothic', 10), fg='#90CAF9',
                 bg=C['header_bg']).pack(side='right', padx=14)
        self._time_lbl = tk.Label(hdr, font=('Malgun Gothic', 9),
                                  fg='#B0BEC5', bg=C['header_bg'])
        self._time_lbl.pack(side='right', padx=16)
        self._tick()

    def _tick(self):
        self._time_lbl.config(text=datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        self.root.after(1000, self._tick)

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=C['sidebar_bg'], width=260)
        sb.pack(side='left', fill='y'); sb.pack_propagate(False)

        menus = [
            ('dashboard',  '대시보드',     '#42A5F5', '🏠'),
            None,
            ('employees',  '인사 관리',    '#1565C0', '👤'),
            ('attendance', '근태 관리',    '#26A69A', '⏱'),
            ('leaves',     '휴가 관리',    '#66BB6A', '🌴'),
            ('payroll',    '급여 관리',    '#FFA726', '💰'),
            None,
        ]

        tk.Label(sb, text="MENU", font=('Malgun Gothic', 11, 'bold'),
                 fg='#78909C', bg=C['sidebar_bg']).pack(pady=(10, 4))

        self._sb_btns = {}; self._sb_meta = {}
        for item in menus:
            if item is None:
                tk.Frame(sb, bg='#B0BEC5', height=1).pack(fill='x', padx=14, pady=2)
                continue
            key, label, color, emoji = item
            self._sb_meta[key] = (color, emoji, label)
            row = tk.Frame(sb, bg=C['sidebar_bg']); row.pack(fill='x', padx=3, pady=0)
            bar = tk.Frame(row, bg=C['sidebar_bg'], width=5); bar.pack(side='left', fill='y')
            btn = tk.Button(row, text=f"  {emoji}  {label}",
                            font=('Malgun Gothic', 14, 'bold'),
                            fg='#000000', bg=C['sidebar_bg'],
                            relief='flat', anchor='w', cursor='hand2', pady=7,
                            activebackground=color, activeforeground='black',
                            command=lambda k=key: self._nav(k))
            btn.pack(side='left', fill='x', expand=True)
            def _on_enter(e, b=btn, c=color, br=bar, k=key):
                if not getattr(self, '_active_key', None) == k:
                    b.config(bg='#CFD8DC', fg='#000000'); br.config(bg=c)
            def _on_leave(e, b=btn, br=bar, k=key):
                if not getattr(self, '_active_key', None) == k:
                    b.config(bg=C['sidebar_bg'], fg='#000000'); br.config(bg=C['sidebar_bg'])
            btn.bind('<Enter>', _on_enter); btn.bind('<Leave>', _on_leave)
            self._sb_btns[key] = (btn, bar)

    def _nav(self, key):
        self._active_key = key
        for k, (b, bar) in self._sb_btns.items():
            color = self._sb_meta[k][0]
            if k == key:
                b.config(bg=color, fg='#000000'); bar.config(bg='#000000')
            else:
                b.config(bg=C['sidebar_bg'], fg='#000000'); bar.config(bg=C['sidebar_bg'])
        for w in self.page_area.winfo_children(): w.destroy()
        if hasattr(self, '_page_canvas'):
            self._page_canvas.yview_moveto(0); self._page_canvas.xview_moveto(0)
        pages = {
            'dashboard':  self._pg_dashboard,
            'employees':  self._pg_employees,
            'attendance': self._pg_attendance,
            'leaves':     self._pg_leaves,
            'payroll':    self._pg_payroll,
        }
        if key in pages: pages[key]()

    # ===========================================
    # 1. 대시보드
    # ===========================================
    def _pg_dashboard(self):
        p = self.page_area
        page_header(p, "대시보드", "  인사 / 근태 / 휴가 / 급여 요약")

        # 통계 카드
        cards = tk.Frame(p, bg=C['bg']); cards.pack(fill='x', padx=20, pady=18)
        today = date.today().isoformat()
        ym = date.today().strftime('%Y-%m')

        emp_cnt = self.db.query("SELECT COUNT(*) FROM employees WHERE active=1 AND status='재직'")[0][0]
        att_today = self.db.query("SELECT COUNT(*) FROM attendance WHERE work_date=?", (today,))[0][0]
        leave_pending = self.db.query("SELECT COUNT(*) FROM leaves WHERE approval='대기'")[0][0]
        pay_total = self.db.query("SELECT COALESCE(SUM(net_pay),0) FROM payrolls WHERE pay_month=?", (ym,))[0][0]

        for title, val, color in [
            ('재직 인원', f"{emp_cnt}명", '#1565C0'),
            ('오늘 출근', f"{att_today}명", '#26A69A'),
            ('휴가 대기', f"{leave_pending}건", '#FFA726'),
            (f'{ym} 급여', f"{int(pay_total):,}원", '#5E35B1'),
        ]:
            card = tk.Frame(cards, bg=color, padx=16, pady=18)
            card.pack(side='left', expand=True, fill='both', padx=6)
            tk.Label(card, text=val, font=('Malgun Gothic', 20, 'bold'),
                     fg='white', bg=color).pack()
            tk.Label(card, text=title, font=('Malgun Gothic', 10),
                     fg='#E0E0E0', bg=color).pack()

        # 부서별 인원
        make_label(p, " 부서별 인원", bold=True, size=11, bg=C['bg']).pack(anchor='w', padx=22, pady=(10, 2))
        wrap = tk.Frame(p, bg=C['bg']); wrap.pack(fill='x', padx=20, pady=4)
        cols = ('부서', '인원수')
        tree = make_tree(wrap, cols, [200, 80], height=6)
        rows = self.db.query("""SELECT COALESCE(dept,'(미정)'), COUNT(*) FROM employees
                                WHERE active=1 AND status='재직' GROUP BY dept ORDER BY COUNT(*) DESC""")
        fill_tree(tree, rows)

        # 휴가 신청 대기
        make_label(p, " 휴가 신청 대기", bold=True, size=11, color=C['warning'], bg=C['bg']).pack(anchor='w', padx=22, pady=(14, 2))
        wrap2 = tk.Frame(p, bg=C['bg']); wrap2.pack(fill='x', padx=20, pady=4)
        cols2 = ('사번', '이름', '구분', '시작일', '종료일', '일수', '사유')
        tree2 = make_tree(wrap2, cols2, [80, 80, 70, 100, 100, 60, 280], height=6)
        rows2 = self.db.query("""SELECT e.emp_no, e.name, l.leave_type, l.start_date, l.end_date,
                                        l.days, COALESCE(l.reason,'')
                                 FROM leaves l LEFT JOIN employees e ON l.emp_id=e.id
                                 WHERE l.approval='대기' ORDER BY l.start_date""")
        fill_tree(tree2, rows2, lambda i, r: 'warn_tag')

    # ===========================================
    # 2. 인사 관리 (Employee Master)
    # ===========================================
    def _pg_employees(self):
        p = self.page_area
        page_header(p, "인사 관리", "  사원 기본정보 — 등록 / 수정 / 삭제")

        f = tk.Frame(p, bg='white', padx=22, pady=18); f.pack(fill='x', padx=20, pady=12)
        vs = {k: tk.StringVar() for k in
              ('emp_no','name','dept','position','join_date','phone','email','base_salary','status')}
        es = {}

        def _lbl(r, c, t):
            make_label(f, t, size=9, color=C['secondary'], bg='white').grid(
                row=r, column=c, sticky='w', padx=6, pady=4)

        _lbl(0, 0, "사번 *");   es['emp_no'] = make_entry(f, vs['emp_no'], 14); es['emp_no'].grid(row=0, column=1, padx=4, pady=8)
        _lbl(0, 2, "이름 *");   es['name']   = make_entry(f, vs['name'], 14); es['name'].grid(row=0, column=3, padx=4, pady=8)
        _lbl(0, 4, "부서");     es['dept']   = make_combo(f, vs['dept'],
            ['생산팀','품질팀','경영지원','영업팀','연구개발','품질관리'], width=14, state='normal'); es['dept'].grid(row=0, column=5, padx=4, pady=8)
        _lbl(0, 6, "직급");     es['position']= make_combo(f, vs['position'],
            ['사원','대리','과장','차장','부장','이사'], width=10, state='normal'); es['position'].grid(row=0, column=7, padx=4, pady=8)

        _lbl(1, 0, "입사일");   vs['join_date'].set(datetime.now().strftime('%Y-%m-%d'))
        es['join_date'] = make_entry(f, vs['join_date'], 14); es['join_date'].grid(row=1, column=1, padx=4, pady=8)
        _lbl(1, 2, "연락처");   es['phone']  = make_entry(f, vs['phone'], 16); es['phone'].grid(row=1, column=3, padx=4, pady=8)
        _lbl(1, 4, "이메일");   es['email']  = make_entry(f, vs['email'], 22); es['email'].grid(row=1, column=5, columnspan=2, padx=4, sticky='w')
        _lbl(1, 7, "재직상태"); es['status'] = make_combo(f, vs['status'], ['재직','휴직','퇴사'], width=10); es['status'].grid(row=1, column=7, padx=4, pady=8); vs['status'].set('재직')

        _lbl(2, 0, "기본급(원)"); es['base_salary'] = make_entry(f, vs['base_salary'], 14); es['base_salary'].grid(row=2, column=1, padx=4, pady=8)

        wrap = tk.Frame(p, bg=C['bg']); wrap.pack(fill='both', expand=True, padx=20, pady=6)
        cols = ('사번','이름','부서','직급','입사일','연락처','이메일','기본급','상태')
        tree = make_tree(wrap, cols, [80, 80, 90, 70, 100, 130, 180, 100, 60], height=14)
        edit_id = [None]

        def _read(key):
            try:
                v = es[key].get()
                if v: return v.strip()
            except: pass
            return (vs[key].get() or '').strip()

        def _load():
            rows = self.db.query("""SELECT emp_no,name,dept,position,join_date,phone,email,base_salary,status
                                    FROM employees WHERE active=1 ORDER BY emp_no""")
            def tag(i, r):
                if r[8] == '퇴사': return 'fail_tag'
                if r[8] == '휴직': return 'warn_tag'
                return 'even' if i%2 else ''
            fill_tree(tree, rows, tag)

        def _clear():
            edit_id[0] = None
            for k in vs: vs[k].set('')
            vs['join_date'].set(datetime.now().strftime('%Y-%m-%d'))
            vs['status'].set('재직')

        def _on_select(e):
            s = tree.selection()
            if not s: return
            v = tree.item(s[0])['values']
            row = self.db.query("SELECT * FROM employees WHERE emp_no=?", (v[0],))
            if not row: return
            r = row[0]
            edit_id[0] = r['id']
            for k in ('emp_no','name','dept','position','join_date','phone','email','status'):
                vs[k].set(str(r[k] or ''))
            vs['base_salary'].set(str(r['base_salary'] or 0))
        tree.bind('<<TreeviewSelect>>', _on_select)

        def _save_new():
            if edit_id[0] is not None:
                if not messagebox.askyesno("확인", "수정 모드입니다.\n신규 등록으로 전환할까요?"):
                    return
                _clear(); return
            no = _read('emp_no'); nm = _read('name')
            if not no or not nm:
                messagebox.showerror("오류", "사번/이름은 필수입니다."); return
            dup = self.db.query("SELECT id FROM employees WHERE emp_no=?", (no,))
            if dup:
                messagebox.showerror("오류", f"사번 {no}는 이미 존재합니다."); return
            try: bs = float(_read('base_salary') or 0)
            except: bs = 0
            try:
                self.db.execute("""INSERT INTO employees(emp_no,name,dept,position,join_date,phone,email,base_salary,status)
                                   VALUES(?,?,?,?,?,?,?,?,?)""",
                                (no, nm, _read('dept'), _read('position'), _read('join_date'),
                                 _read('phone'), _read('email'), bs, _read('status') or '재직'))
            except Exception as e:
                messagebox.showerror("저장 실패", f"{e}"); return
            messagebox.showinfo("완료", f"사원 [{nm}] 등록 완료!")
            _clear(); _load()

        def _update():
            if edit_id[0] is None:
                messagebox.showwarning("수정", "수정할 사원을 목록에서 선택하세요."); return
            try: bs = float(_read('base_salary') or 0)
            except: bs = 0
            self.db.execute("""UPDATE employees SET emp_no=?,name=?,dept=?,position=?,
                               join_date=?,phone=?,email=?,base_salary=?,status=?
                               WHERE id=?""",
                            (_read('emp_no'), _read('name'), _read('dept'), _read('position'),
                             _read('join_date'), _read('phone'), _read('email'), bs,
                             _read('status'), edit_id[0]))
            messagebox.showinfo("완료", "사원 정보 수정 완료!")
            _clear(); _load()

        def _delete():
            if edit_id[0] is None:
                messagebox.showwarning("삭제", "삭제할 사원을 선택하세요."); return
            if not messagebox.askyesno("삭제 확인", "사원을 삭제(비활성화)하시겠습니까?"):
                return
            self.db.execute("UPDATE employees SET active=0 WHERE id=?", (edit_id[0],))
            messagebox.showinfo("완료", "삭제(비활성화) 완료!")
            _clear(); _load()

        btn_row = tk.Frame(f, bg='white')
        btn_row.grid(row=3, column=0, columnspan=8, sticky='e', pady=(12, 0))
        color_btn(btn_row, "사원 등록", _save_new, theme='save').pack(side='right', padx=5)
        color_btn(btn_row, "사원 수정", _update, theme='update').pack(side='right', padx=5)
        color_btn(btn_row, "사원 삭제", _delete, theme='delete').pack(side='right', padx=5)

        _reset_bar = tk.Frame(p, bg=C['bg']); _reset_bar.pack(side='bottom', fill='x', padx=20, pady=8)
        color_btn(_reset_bar, "초기화", _clear, theme='neutral', size=9, padx=10, pady=5).pack(side='right')
        self.root.bind('<Escape>', lambda e: _clear())
        _load()

    # ===========================================
    # 3. 근태 관리 (Attendance Log)
    # ===========================================
    def _pg_attendance(self):
        p = self.page_area
        page_header(p, "근태 관리", "  출근/퇴근 자동 기록 + 근무시간 자동 계산")

        emps = self.db.query("SELECT id,emp_no,name FROM employees WHERE active=1 ORDER BY emp_no")
        emp_disp = [f"{r[1]} {r[2]}" for r in emps]

        # ── 1. 출근/퇴근 자동 기록 패널 ──
        auto = tk.Frame(p, bg='#E0F2F1', padx=20, pady=18)
        auto.pack(fill='x', padx=20, pady=(12, 4))

        tk.Label(auto, text="⏱  출근 / 퇴근 자동 기록",
                 font=('Malgun Gothic', 14, 'bold'),
                 fg=C['primary_dark'], bg='#E0F2F1').pack(side='left', padx=(0, 16))

        # 실시간 시계
        clock_lbl = tk.Label(auto, text='--:--:--',
                             font=('Menlo', 24, 'bold'),
                             fg=C['accent'], bg='#E0F2F1')
        clock_lbl.pack(side='left', padx=10)

        def _tick_clock():
            try:
                clock_lbl.config(text=datetime.now().strftime('%H:%M:%S'))
                clock_lbl.after(1000, _tick_clock)
            except: pass
        _tick_clock()

        # 사원 선택
        tk.Label(auto, text="사원:", font=('Malgun Gothic', 11, 'bold'),
                 bg='#E0F2F1').pack(side='left', padx=(20, 4))
        auto_emp_v = tk.StringVar()
        auto_emp_combo = ttk.Combobox(auto, textvariable=auto_emp_v,
                                       values=emp_disp, state='readonly',
                                       width=16, font=('Malgun Gothic', 11))
        auto_emp_combo.pack(side='left', padx=4)

        # 상태 표시
        status_lbl = tk.Label(auto, text='',
                              font=('Malgun Gothic', 10, 'bold'),
                              bg='#E0F2F1', fg=C['secondary'])
        status_lbl.pack(side='left', padx=12)

        def _resolve_emp_id(disp):
            if not disp or disp not in emp_disp: return None
            return emps[emp_disp.index(disp)][0]

        def _today_record(emp_id):
            today = date.today().isoformat()
            r = self.db.query("""SELECT id,check_in,check_out FROM attendance
                                 WHERE emp_id=? AND work_date=? ORDER BY id DESC LIMIT 1""",
                              (emp_id, today))
            return r[0] if r else None

        def _refresh_status(*_):
            disp = auto_emp_v.get()
            emp_id = _resolve_emp_id(disp)
            if not emp_id:
                status_lbl.config(text=''); return
            rec = _today_record(emp_id)
            if not rec:
                status_lbl.config(text='⚪ 미출근', fg='#90A4AE')
            elif rec[1] and not rec[2]:
                status_lbl.config(text=f'🟢 출근 {rec[1]} (근무중)', fg=C['success'])
            elif rec[1] and rec[2]:
                status_lbl.config(text=f'✅ 출근 {rec[1]} → 퇴근 {rec[2]}', fg=C['primary'])
            else:
                status_lbl.config(text='⚪ 미출근', fg='#90A4AE')
        auto_emp_combo.bind('<<ComboboxSelected>>', _refresh_status)

        def _calc(ci, co):
            try:
                ti = datetime.strptime(ci, '%H:%M'); to = datetime.strptime(co, '%H:%M')
                hours = (to - ti).total_seconds() / 3600
                if hours < 0: hours += 24
                if hours > 4: hours -= 1  # 점심 1h 차감
                ot = max(0, hours - 8); base = min(hours, 8)
                return round(base, 2), round(ot, 2)
            except: return 0, 0

        def _check_in():
            disp = auto_emp_v.get()
            emp_id = _resolve_emp_id(disp)
            if not emp_id:
                messagebox.showerror("출근", "사원을 선택하세요."); return
            rec = _today_record(emp_id)
            if rec and rec[1]:
                messagebox.showwarning("출근",
                    f"오늘 이미 출근 기록이 있습니다.\n출근시각: {rec[1]}"); return
            now_s = datetime.now().strftime('%H:%M')
            today = date.today().isoformat()
            # 9시 이후 출근이면 '지각'
            status = '정상'
            try:
                if datetime.strptime(now_s, '%H:%M') > datetime.strptime('09:00', '%H:%M'):
                    status = '지각'
            except: pass
            self.db.execute("""INSERT INTO attendance(emp_id,work_date,check_in,status)
                               VALUES(?,?,?,?)""", (emp_id, today, now_s, status))
            messagebox.showinfo("출근 완료",
                f"✅ {disp.split(' ',1)[1] if ' ' in disp else disp} 님\n"
                f"출근 시각: {now_s}\n상태: {status}")
            _refresh_status(); _load()

        def _check_out():
            disp = auto_emp_v.get()
            emp_id = _resolve_emp_id(disp)
            if not emp_id:
                messagebox.showerror("퇴근", "사원을 선택하세요."); return
            rec = _today_record(emp_id)
            if not rec or not rec[1]:
                messagebox.showwarning("퇴근",
                    "오늘 출근 기록이 없습니다.\n먼저 [🟢 출근] 버튼을 눌러주세요."); return
            if rec[2]:
                messagebox.showwarning("퇴근",
                    f"오늘 이미 퇴근했습니다.\n퇴근시각: {rec[2]}"); return
            now_s = datetime.now().strftime('%H:%M')
            wh, ot = _calc(rec[1], now_s)
            self.db.execute("""UPDATE attendance SET check_out=?, work_hours=?, overtime_hours=?
                               WHERE id=?""", (now_s, wh, ot, rec[0]))
            messagebox.showinfo("퇴근 완료",
                f"✅ {disp.split(' ',1)[1] if ' ' in disp else disp} 님\n"
                f"퇴근 시각: {now_s}\n근무 {wh}h / 초과 {ot}h")
            _refresh_status(); _load()

        # 출근/퇴근 버튼
        color_btn(auto, "🟢 출근", _check_in, theme='save', size=14, padx=24, pady=10).pack(side='left', padx=(20, 6))
        color_btn(auto, "🔴 퇴근", _check_out, theme='delete', size=14, padx=24, pady=10).pack(side='left', padx=6)

        # ── 2. 수동 등록 폼 ──
        tk.Label(p, text=" 수동 등록 / 수정 (특별 케이스용)",
                 font=('Malgun Gothic', 11, 'bold'),
                 fg=C['secondary'], bg=C['bg']).pack(anchor='w', padx=22, pady=(10, 2))

        f = tk.Frame(p, bg='white', padx=22, pady=14); f.pack(fill='x', padx=20, pady=4)
        def _lbl(r, c, t):
            make_label(f, t, size=9, color=C['secondary'], bg='white').grid(row=r, column=c, sticky='w', padx=6, pady=10)

        _lbl(0, 0, "사원 *")
        emp_v = tk.StringVar()
        emp_e = make_combo(f, emp_v, emp_disp, width=20); emp_e.grid(row=0, column=1, padx=4, pady=8)

        _lbl(0, 2, "근무일 *")
        dt_v = tk.StringVar(value=date.today().isoformat())
        dt_e = make_entry(f, dt_v, 14); dt_e.grid(row=0, column=3, padx=4, pady=8)

        _lbl(0, 4, "출근 (HH:MM)")
        in_v = tk.StringVar(value='09:00')
        in_e = make_entry(f, in_v, 10); in_e.grid(row=0, column=5, padx=4, pady=8)

        _lbl(0, 6, "퇴근 (HH:MM)")
        out_v = tk.StringVar(value='18:00')
        out_e = make_entry(f, out_v, 10); out_e.grid(row=0, column=7, padx=4, pady=8)

        _lbl(1, 0, "상태")
        st_v = tk.StringVar(value='정상')
        st_e = make_combo(f, st_v, ['정상','지각','조퇴','결근','반차','출장'], width=12); st_e.grid(row=1, column=1, padx=4, pady=8)

        _lbl(1, 2, "비고")
        m_v = tk.StringVar()
        m_e = make_entry(f, m_v, 36); m_e.grid(row=1, column=3, columnspan=4, padx=4, sticky='w')

        wrap = tk.Frame(p, bg=C['bg']); wrap.pack(fill='both', expand=True, padx=20, pady=6)
        cols = ('AID','근무일','사번','이름','출근','퇴근','근무시간','초과','상태','비고')
        tree = make_tree(wrap, cols, [0, 100, 80, 80, 70, 70, 80, 70, 70, 200], height=14)
        tree.column('AID', width=0, stretch=False)
        edit_id = [None]

        def _read(w, v, default=''):
            try:
                x = w.get()
                if x: return x.strip()
            except: pass
            return (v.get() or default).strip()

        def _calc_hours(ci, co):
            try:
                fmt = '%H:%M'
                ti = datetime.strptime(ci, fmt); to = datetime.strptime(co, fmt)
                hours = (to - ti).total_seconds() / 3600
                if hours < 0: hours += 24
                # 점심시간 1시간 차감
                if hours > 4: hours -= 1
                ot = max(0, hours - 8)  # 8시간 초과분
                base = min(hours, 8)
                return round(base, 2), round(ot, 2)
            except: return 0, 0

        def _load():
            rows = self.db.query("""SELECT a.id, a.work_date, e.emp_no, e.name,
                                           a.check_in, a.check_out, a.work_hours,
                                           a.overtime_hours, a.status, COALESCE(a.memo,'')
                                    FROM attendance a LEFT JOIN employees e ON a.emp_id=e.id
                                    ORDER BY a.work_date DESC, a.id DESC LIMIT 200""")
            def tag(i, r):
                if r[8] in ('결근','지각'): return 'fail_tag'
                if r[8] in ('반차','조퇴'): return 'warn_tag'
                return 'even' if i%2 else ''
            fill_tree(tree, rows, tag)

        def _clear():
            edit_id[0] = None
            emp_v.set(''); m_v.set(''); st_v.set('정상')
            dt_v.set(date.today().isoformat())
            in_v.set('09:00'); out_v.set('18:00')

        def _on_sel(e):
            s = tree.selection()
            if not s: return
            v = tree.item(s[0])['values']
            edit_id[0] = v[0]
            dt_v.set(str(v[1])); in_v.set(str(v[4])); out_v.set(str(v[5]))
            st_v.set(str(v[8])); m_v.set(str(v[9]))
            for d in emp_disp:
                if d.startswith(str(v[2])):
                    emp_v.set(d); break
        tree.bind('<<TreeviewSelect>>', _on_sel)

        def _save_new():
            if edit_id[0] is not None:
                if not messagebox.askyesno("확인", "수정 모드입니다.\n신규로 전환할까요?"):
                    return
                _clear(); return
            ev = _read(emp_e, emp_v)
            if not ev:
                messagebox.showerror("오류", "사원을 선택하세요."); return
            emp_id = emps[emp_disp.index(ev)][0] if ev in emp_disp else None
            if not emp_id:
                messagebox.showerror("오류", "유효한 사원이 아닙니다."); return
            dt = _read(dt_e, dt_v); ci = _read(in_e, in_v); co = _read(out_e, out_v)
            wh, ot = _calc_hours(ci, co)
            self.db.execute("""INSERT INTO attendance(emp_id,work_date,check_in,check_out,
                               work_hours,overtime_hours,status,memo) VALUES(?,?,?,?,?,?,?,?)""",
                            (emp_id, dt, ci, co, wh, ot, _read(st_e, st_v), _read(m_e, m_v)))
            messagebox.showinfo("완료", f"근태 등록! (근무 {wh}h, 초과 {ot}h)")
            _clear(); _load()

        def _update():
            if edit_id[0] is None:
                messagebox.showwarning("수정", "수정할 행을 선택하세요."); return
            ci = _read(in_e, in_v); co = _read(out_e, out_v)
            wh, ot = _calc_hours(ci, co)
            self.db.execute("""UPDATE attendance SET work_date=?,check_in=?,check_out=?,
                               work_hours=?,overtime_hours=?,status=?,memo=? WHERE id=?""",
                            (_read(dt_e, dt_v), ci, co, wh, ot,
                             _read(st_e, st_v), _read(m_e, m_v), edit_id[0]))
            messagebox.showinfo("완료", "근태 수정 완료!")
            _clear(); _load()

        def _delete():
            if edit_id[0] is None:
                messagebox.showwarning("삭제", "삭제할 행을 선택하세요."); return
            if not messagebox.askyesno("삭제", "이 근태 기록을 삭제하시겠습니까?"): return
            self.db.execute("DELETE FROM attendance WHERE id=?", (edit_id[0],))
            messagebox.showinfo("완료", "삭제 완료!")
            _clear(); _load()

        btn_row = tk.Frame(f, bg='white')
        btn_row.grid(row=2, column=0, columnspan=8, sticky='e', pady=(12, 0))
        color_btn(btn_row, "근태 등록", _save_new, theme='save').pack(side='right', padx=5)
        color_btn(btn_row, "근태 수정", _update, theme='update').pack(side='right', padx=5)
        color_btn(btn_row, "근태 삭제", _delete, theme='delete').pack(side='right', padx=5)

        _reset_bar = tk.Frame(p, bg=C['bg']); _reset_bar.pack(side='bottom', fill='x', padx=20, pady=8)
        color_btn(_reset_bar, "초기화", _clear, theme='neutral', size=9, padx=10, pady=5).pack(side='right')
        self.root.bind('<Escape>', lambda e: _clear())
        _load()

    # ===========================================
    # 4. 휴가 관리 (Leave Management)
    # ===========================================
    def _pg_leaves(self):
        p = self.page_area
        page_header(p, "휴가 관리", "  연차 / 병가 / 휴직 신청 및 승인")

        emps = self.db.query("SELECT id,emp_no,name FROM employees WHERE active=1 ORDER BY emp_no")
        emp_disp = [f"{r[1]} {r[2]}" for r in emps]

        f = tk.Frame(p, bg='white', padx=22, pady=18); f.pack(fill='x', padx=20, pady=12)
        def _lbl(r, c, t):
            make_label(f, t, size=9, color=C['secondary'], bg='white').grid(row=r, column=c, sticky='w', padx=6, pady=10)

        _lbl(0, 0, "사원 *")
        emp_v = tk.StringVar()
        emp_e = make_combo(f, emp_v, emp_disp, width=20); emp_e.grid(row=0, column=1, padx=4, pady=8)

        _lbl(0, 2, "구분 *")
        type_v = tk.StringVar(value='연차')
        type_e = make_combo(f, type_v, ['연차','반차','병가','경조사','휴직','기타'], width=12); type_e.grid(row=0, column=3, padx=4, pady=8)

        _lbl(0, 4, "시작일 *")
        sd_v = tk.StringVar(value=date.today().isoformat())
        sd_e = make_entry(f, sd_v, 14); sd_e.grid(row=0, column=5, padx=4, pady=8)

        _lbl(0, 6, "종료일 *")
        ed_v = tk.StringVar(value=date.today().isoformat())
        ed_e = make_entry(f, ed_v, 14); ed_e.grid(row=0, column=7, padx=4, pady=8)

        _lbl(1, 0, "사유")
        rsn_v = tk.StringVar()
        rsn_e = make_entry(f, rsn_v, 36); rsn_e.grid(row=1, column=1, columnspan=4, padx=4, sticky='w')

        _lbl(1, 5, "승인상태")
        ap_v = tk.StringVar(value='대기')
        ap_e = make_combo(f, ap_v, ['대기','승인','반려','취소'], width=10); ap_e.grid(row=1, column=6, padx=4)

        wrap = tk.Frame(p, bg=C['bg']); wrap.pack(fill='both', expand=True, padx=20, pady=6)
        cols = ('LID','사번','이름','구분','시작','종료','일수','사유','상태')
        tree = make_tree(wrap, cols, [0, 80, 80, 70, 100, 100, 60, 230, 70], height=14)
        tree.column('LID', width=0, stretch=False)
        edit_id = [None]

        def _read(w, v, default=''):
            try:
                x = w.get()
                if x: return x.strip()
            except: pass
            return (v.get() or default).strip()

        def _calc_days(s, e):
            try:
                d1 = datetime.strptime(s, '%Y-%m-%d').date()
                d2 = datetime.strptime(e, '%Y-%m-%d').date()
                return max(1, (d2 - d1).days + 1)
            except: return 1

        def _load():
            rows = self.db.query("""SELECT l.id, e.emp_no, e.name, l.leave_type,
                                           l.start_date, l.end_date, l.days,
                                           COALESCE(l.reason,''), l.approval
                                    FROM leaves l LEFT JOIN employees e ON l.emp_id=e.id
                                    ORDER BY l.start_date DESC LIMIT 200""")
            def tag(i, r):
                if r[8] == '승인': return 'pass_tag'
                if r[8] == '반려': return 'fail_tag'
                if r[8] == '대기': return 'warn_tag'
                return 'even' if i%2 else ''
            fill_tree(tree, rows, tag)

        def _clear():
            edit_id[0] = None
            emp_v.set(''); type_v.set('연차'); rsn_v.set(''); ap_v.set('대기')
            sd_v.set(date.today().isoformat()); ed_v.set(date.today().isoformat())

        def _on_sel(e):
            s = tree.selection()
            if not s: return
            v = tree.item(s[0])['values']
            edit_id[0] = v[0]
            type_v.set(str(v[3])); sd_v.set(str(v[4])); ed_v.set(str(v[5]))
            rsn_v.set(str(v[7])); ap_v.set(str(v[8]))
            for d in emp_disp:
                if d.startswith(str(v[1])):
                    emp_v.set(d); break
        tree.bind('<<TreeviewSelect>>', _on_sel)

        def _save_new():
            if edit_id[0] is not None:
                if not messagebox.askyesno("확인", "수정 모드. 신규로 전환할까요?"): return
                _clear(); return
            ev = _read(emp_e, emp_v)
            if not ev or ev not in emp_disp:
                messagebox.showerror("오류", "유효한 사원을 선택하세요."); return
            emp_id = emps[emp_disp.index(ev)][0]
            sd = _read(sd_e, sd_v); ed = _read(ed_e, ed_v)
            days = _calc_days(sd, ed)
            self.db.execute("""INSERT INTO leaves(emp_id,leave_type,start_date,end_date,
                               days,reason,approval) VALUES(?,?,?,?,?,?,?)""",
                            (emp_id, _read(type_e, type_v), sd, ed, days,
                             _read(rsn_e, rsn_v), _read(ap_e, ap_v)))
            messagebox.showinfo("완료", f"휴가 신청! ({days}일)")
            _clear(); _load()

        def _update():
            if edit_id[0] is None:
                messagebox.showwarning("수정", "수정할 행을 선택하세요."); return
            sd = _read(sd_e, sd_v); ed = _read(ed_e, ed_v); days = _calc_days(sd, ed)
            self.db.execute("""UPDATE leaves SET leave_type=?,start_date=?,end_date=?,days=?,
                               reason=?,approval=? WHERE id=?""",
                            (_read(type_e, type_v), sd, ed, days,
                             _read(rsn_e, rsn_v), _read(ap_e, ap_v), edit_id[0]))
            messagebox.showinfo("완료", "휴가 수정 완료!")
            _clear(); _load()

        def _delete():
            if edit_id[0] is None:
                messagebox.showwarning("삭제", "삭제할 행을 선택하세요."); return
            if not messagebox.askyesno("삭제", "삭제하시겠습니까?"): return
            self.db.execute("DELETE FROM leaves WHERE id=?", (edit_id[0],))
            messagebox.showinfo("완료", "삭제 완료!")
            _clear(); _load()

        def _approve():
            if edit_id[0] is None:
                messagebox.showwarning("승인", "처리할 행을 선택하세요."); return
            self.db.execute("UPDATE leaves SET approval='승인' WHERE id=?", (edit_id[0],))
            messagebox.showinfo("승인", "휴가가 승인되었습니다.")
            _clear(); _load()

        btn_row = tk.Frame(f, bg='white')
        btn_row.grid(row=2, column=0, columnspan=8, sticky='e', pady=(12, 0))
        color_btn(btn_row, "휴가 신청", _save_new, theme='save').pack(side='right', padx=5)
        color_btn(btn_row, "휴가 수정", _update, theme='update').pack(side='right', padx=5)
        color_btn(btn_row, "휴가 삭제", _delete, theme='delete').pack(side='right', padx=5)
        color_btn(btn_row, "✓ 승인", _approve, theme='action').pack(side='right', padx=5)

        _reset_bar = tk.Frame(p, bg=C['bg']); _reset_bar.pack(side='bottom', fill='x', padx=20, pady=8)
        color_btn(_reset_bar, "초기화", _clear, theme='neutral', size=9, padx=10, pady=5).pack(side='right')
        self.root.bind('<Escape>', lambda e: _clear())
        _load()

    # ===========================================
    # 5. 급여 관리 (Payroll)
    # ===========================================
    def _pg_payroll(self):
        p = self.page_area
        page_header(p, "급여 관리", "  기본급 + 초과수당 - 공제 = 실수령액")

        emps = self.db.query("SELECT id,emp_no,name,base_salary FROM employees WHERE active=1 ORDER BY emp_no")
        emp_disp = [f"{r[1]} {r[2]}" for r in emps]

        f = tk.Frame(p, bg='white', padx=22, pady=18); f.pack(fill='x', padx=20, pady=12)
        def _lbl(r, c, t):
            make_label(f, t, size=9, color=C['secondary'], bg='white').grid(row=r, column=c, sticky='w', padx=6, pady=10)

        _lbl(0, 0, "사원 *")
        emp_v = tk.StringVar()
        emp_e = make_combo(f, emp_v, emp_disp, width=20); emp_e.grid(row=0, column=1, padx=4, pady=8)

        _lbl(0, 2, "급여월 *")
        pm_v = tk.StringVar(value=date.today().strftime('%Y-%m'))
        pm_e = make_entry(f, pm_v, 12); pm_e.grid(row=0, column=3, padx=4, pady=8)

        _lbl(0, 4, "지급일")
        pd_v = tk.StringVar(value=date.today().isoformat())
        pd_e = make_entry(f, pd_v, 14); pd_e.grid(row=0, column=5, padx=4, pady=8)

        _lbl(1, 0, "기본급(원)")
        base_v = tk.StringVar(value='0')
        base_e = make_entry(f, base_v, 14); base_e.grid(row=1, column=1, padx=4, pady=8)

        _lbl(1, 2, "초과수당")
        ot_v = tk.StringVar(value='0')
        ot_e = make_entry(f, ot_v, 14); ot_e.grid(row=1, column=3, padx=4, pady=8)

        _lbl(1, 4, "상여금")
        bn_v = tk.StringVar(value='0')
        bn_e = make_entry(f, bn_v, 14); bn_e.grid(row=1, column=5, padx=4, pady=8)

        _lbl(1, 6, "공제(세금/4대보험)")
        ded_v = tk.StringVar(value='0')
        ded_e = make_entry(f, ded_v, 14); ded_e.grid(row=1, column=7, padx=4, pady=8)

        _lbl(2, 0, "비고")
        m_v = tk.StringVar()
        m_e = make_entry(f, m_v, 36); m_e.grid(row=2, column=1, columnspan=4, padx=4, sticky='w')

        net_lbl = tk.Label(f, text="실수령액: 0원",
                           font=('Malgun Gothic', 14, 'bold'),
                           fg=C['primary'], bg='white')
        net_lbl.grid(row=2, column=5, columnspan=3, sticky='e', padx=10)

        # 사원 선택 시 기본급 자동 채움
        def _on_emp(e=None):
            if emp_v.get() in emp_disp:
                idx = emp_disp.index(emp_v.get())
                base_v.set(str(int(emps[idx][3] or 0)))
                _calc()
        emp_e.bind('<<ComboboxSelected>>', _on_emp)

        def _calc(*_):
            try:
                b = float(base_v.get() or 0); o = float(ot_v.get() or 0)
                bn = float(bn_v.get() or 0); d = float(ded_v.get() or 0)
                net = b + o + bn - d
                net_lbl.config(text=f"실수령액: {int(net):,}원")
            except: pass
        for v in (base_v, ot_v, bn_v, ded_v): v.trace_add('write', _calc)

        wrap = tk.Frame(p, bg=C['bg']); wrap.pack(fill='both', expand=True, padx=20, pady=6)
        cols = ('PID','월','사번','이름','기본급','초과','상여','공제','실수령','지급일')
        tree = make_tree(wrap, cols, [0, 80, 80, 80, 100, 80, 80, 80, 110, 100], height=14)
        tree.column('PID', width=0, stretch=False)
        edit_id = [None]

        def _read(w, v, default=''):
            try:
                x = w.get()
                if x: return x.strip()
            except: pass
            return (v.get() or default).strip()

        def _load():
            rows = self.db.query("""SELECT p.id, p.pay_month, e.emp_no, e.name,
                                           p.base_salary, p.overtime_pay, p.bonus,
                                           p.deduction, p.net_pay, p.paid_date
                                    FROM payrolls p LEFT JOIN employees e ON p.emp_id=e.id
                                    ORDER BY p.pay_month DESC, p.id DESC LIMIT 200""")
            # 금액 포맷
            disp = []
            for r in rows:
                d = list(r)
                for i in (4,5,6,7,8): d[i] = f"{int(d[i] or 0):,}"
                disp.append(d)
            fill_tree(tree, disp)

        def _clear():
            edit_id[0] = None
            emp_v.set(''); m_v.set('')
            for v in (base_v, ot_v, bn_v, ded_v): v.set('0')
            pm_v.set(date.today().strftime('%Y-%m'))
            pd_v.set(date.today().isoformat())
            net_lbl.config(text="실수령액: 0원")

        def _on_sel(e):
            s = tree.selection()
            if not s: return
            v = tree.item(s[0])['values']
            edit_id[0] = v[0]
            row = self.db.query("SELECT * FROM payrolls WHERE id=?", (v[0],))[0]
            pm_v.set(str(row['pay_month'])); pd_v.set(str(row['paid_date'] or ''))
            base_v.set(str(int(row['base_salary'] or 0)))
            ot_v.set(str(int(row['overtime_pay'] or 0)))
            bn_v.set(str(int(row['bonus'] or 0)))
            ded_v.set(str(int(row['deduction'] or 0)))
            m_v.set(str(row['memo'] or ''))
            for d in emp_disp:
                if d.startswith(str(v[2])):
                    emp_v.set(d); break
        tree.bind('<<TreeviewSelect>>', _on_sel)

        def _save_new():
            if edit_id[0] is not None:
                if not messagebox.askyesno("확인", "수정 모드. 신규로 전환?"): return
                _clear(); return
            ev = _read(emp_e, emp_v)
            if not ev or ev not in emp_disp:
                messagebox.showerror("오류", "사원을 선택하세요."); return
            emp_id = emps[emp_disp.index(ev)][0]
            try:
                b = float(_read(base_e, base_v) or 0); o = float(_read(ot_e, ot_v) or 0)
                bn = float(_read(bn_e, bn_v) or 0); d = float(_read(ded_e, ded_v) or 0)
            except:
                messagebox.showerror("오류", "금액은 숫자로 입력하세요."); return
            net = b + o + bn - d
            self.db.execute("""INSERT INTO payrolls(emp_id,pay_month,base_salary,overtime_pay,
                               bonus,deduction,net_pay,paid_date,memo)
                               VALUES(?,?,?,?,?,?,?,?,?)""",
                            (emp_id, _read(pm_e, pm_v), b, o, bn, d, net,
                             _read(pd_e, pd_v), _read(m_e, m_v)))
            messagebox.showinfo("완료", f"급여 등록! 실수령액 {int(net):,}원")
            _clear(); _load()

        def _update():
            if edit_id[0] is None:
                messagebox.showwarning("수정", "수정할 행을 선택하세요."); return
            try:
                b = float(_read(base_e, base_v) or 0); o = float(_read(ot_e, ot_v) or 0)
                bn = float(_read(bn_e, bn_v) or 0); d = float(_read(ded_e, ded_v) or 0)
            except:
                messagebox.showerror("오류", "금액은 숫자로 입력하세요."); return
            net = b + o + bn - d
            self.db.execute("""UPDATE payrolls SET pay_month=?,base_salary=?,overtime_pay=?,
                               bonus=?,deduction=?,net_pay=?,paid_date=?,memo=? WHERE id=?""",
                            (_read(pm_e, pm_v), b, o, bn, d, net,
                             _read(pd_e, pd_v), _read(m_e, m_v), edit_id[0]))
            messagebox.showinfo("완료", "급여 수정 완료!")
            _clear(); _load()

        def _delete():
            if edit_id[0] is None:
                messagebox.showwarning("삭제", "삭제할 행을 선택하세요."); return
            if not messagebox.askyesno("삭제", "삭제하시겠습니까?"): return
            self.db.execute("DELETE FROM payrolls WHERE id=?", (edit_id[0],))
            messagebox.showinfo("완료", "삭제 완료!")
            _clear(); _load()

        btn_row = tk.Frame(f, bg='white')
        btn_row.grid(row=3, column=0, columnspan=8, sticky='e', pady=(12, 0))
        color_btn(btn_row, "급여 등록", _save_new, theme='save').pack(side='right', padx=5)
        color_btn(btn_row, "급여 수정", _update, theme='update').pack(side='right', padx=5)
        color_btn(btn_row, "급여 삭제", _delete, theme='delete').pack(side='right', padx=5)

        _reset_bar = tk.Frame(p, bg=C['bg']); _reset_bar.pack(side='bottom', fill='x', padx=20, pady=8)
        color_btn(_reset_bar, "초기화", _clear, theme='neutral', size=9, padx=10, pady=5).pack(side='right')
        self.root.bind('<Escape>', lambda e: _clear())
        _load()


# ────────────────────────────────────────
if __name__ == '__main__':
    if sys.platform == 'win32':
        try: sys.stdout.reconfigure(encoding='utf-8')
        except: pass
    HRApp()
