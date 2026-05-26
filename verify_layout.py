import tkinter as tk

# 테스트할 레이아웃 재현
root = tk.Tk()
root.geometry("1340x820")

# 헤더 (56px 고정)
header = tk.Frame(root, bg='#1565C0', height=56)
header.pack(fill='x')
header.pack_propagate(False)
tk.Label(header, text="헤더 (56px)", bg='#1565C0', fg='white', 
         font=('Malgun Gothic', 12)).pack(side='left', padx=20, pady=10)

# 콘텐츠 프레임
content = tk.Frame(root, bg='white')
content.pack(fill='both', expand=True)

# ===== 좌측: 사이드바 =====
sidebar = tk.Frame(content, bg='#ECEFF1', width=230)
sidebar.pack(side='left', fill='y', anchor='nw')
sidebar.pack_propagate(False)

# MENU 라벨 (높이 24px 고정)
menu_frame = tk.Frame(sidebar, bg='#ECEFF1', height=24)
menu_frame.pack(fill='x')
menu_frame.pack_propagate(False)
menu_label = tk.Label(menu_frame, text="MENU", font=('Malgun Gothic', 18, 'bold'),
                      fg='#78909C', bg='#ECEFF1')
menu_label.pack(pady=(0, 0))

# 첫 번째 메뉴 버튼
btn_frame = tk.Frame(sidebar, bg='#ECEFF1')
btn_frame.pack(fill='x', padx=3, pady=0)
bar = tk.Frame(btn_frame, bg='#ECEFF1', width=5)
bar.pack(side='left', fill='y')
btn = tk.Button(btn_frame, text="  🏠  대시보드", font=('Malgun Gothic', 18, 'bold'),
               fg='#000000', bg='#ECEFF1', relief='flat', anchor='w', pady=2)
btn.pack(side='left', fill='x', expand=True)

sidebar_label = tk.Label(sidebar, text="← 좌측: menu_frame(24px) + 버튼", 
                        fg='#666666', bg='#ECEFF1', font=('Malgun Gothic', 9))
sidebar_label.pack(anchor='w', padx=10, pady=10)

# ===== 우측: 페이지 콘텐츠 =====
page_area = tk.Frame(content, bg='white')
page_area.pack(side='left', fill='both', expand=True)

# 스페이서 (높이 24px 고정)
spacer = tk.Frame(page_area, bg='white', height=24)
spacer.pack(fill='x')
spacer.pack_propagate(False)

# 제목 프레임
title_frame = tk.Frame(page_area, bg='white')
title_frame.pack(fill='x', pady=(0, 0))
title_label = tk.Label(title_frame, text="근태관리", font=('Malgun Gothic', 18, 'bold'),
                      fg='#1565C0', bg='white')
title_label.pack(side='left', padx=24, pady=(0, 2))

page_label = tk.Label(page_area, text="→ 우측: spacer(24px) + 제목", 
                     fg='#666666', bg='white', font=('Malgun Gothic', 9))
page_label.pack(anchor='w', padx=24, pady=10)

# 검증 라벨
verify_frame = tk.Frame(root, bg='#FFF9C4', height=60)
verify_frame.pack(fill='x')
verify_frame.pack_propagate(False)

verify_text = """
✓ 좌측 menu_frame 높이: 24px (pack_propagate=False)
✓ 우측 spacer 높이: 24px (pack_propagate=False)
✓ 첫 버튼과 제목이 같은 y좌표에서 시작되어야 함

실제 화면에서 "대시보드"와 "근태관리"의 텍스트 정렬을 확인하세요.
"""

tk.Label(verify_frame, text=verify_text, font=('Malgun Gothic', 10),
        bg='#FFF9C4', justify='left').pack(side='left', padx=20, pady=8)

root.mainloop()
