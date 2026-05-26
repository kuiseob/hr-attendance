#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO JIN PRECISION CO. 인사/근태 관리 시스템 - 사용자 매뉴얼 생성기
출력: SEOJIN_HR_사용자매뉴얼.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

# ── 폰트 등록 ──────────────────────────────────────────────────────────────
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
]
FONT_NAME = "KR"
font_registered = False
for fp in FONT_PATHS:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont(FONT_NAME, fp))
            font_registered = True
            print(f"Font loaded: {fp}")
            break
        except Exception:
            continue
if not font_registered:
    FONT_NAME = "Helvetica"
    print("Warning: Korean font not found, using Helvetica")

# ── 색상 팔레트 ────────────────────────────────────────────────────────────
BLUE     = colors.HexColor("#1565C0")
BLUE_LT  = colors.HexColor("#E3F2FD")
TEAL     = colors.HexColor("#26A69A")
ORANGE   = colors.HexColor("#FFA726")
PURPLE   = colors.HexColor("#5E35B1")
GREEN    = colors.HexColor("#66BB6A")
GRAY     = colors.HexColor("#607D8B")
GRAY_LT  = colors.HexColor("#F5F5F5")
RED      = colors.HexColor("#E53935")
BLACK    = colors.black
WHITE    = colors.white

W, H = A4  # 595.27 x 841.89 pts

# ── 스타일 ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    kw.setdefault('fontName', FONT_NAME)
    return ParagraphStyle(name, **kw)

sTitle    = S("Title",   fontSize=28, textColor=WHITE, leading=36, alignment=TA_CENTER, spaceAfter=8)
sSub      = S("Sub",     fontSize=13, textColor=BLUE_LT, leading=18, alignment=TA_CENTER)
sH1       = S("H1",      fontSize=16, textColor=WHITE,    leading=22, spaceBefore=4, spaceAfter=2)
sH2       = S("H2",      fontSize=13, textColor=BLUE,     leading=18, spaceBefore=10, spaceAfter=4, leftIndent=4)
sH3       = S("H3",      fontSize=11, textColor=TEAL,     leading=15, spaceBefore=6,  spaceAfter=2, leftIndent=8)
sBody     = S("Body",    fontSize=10, textColor=BLACK,    leading=16, spaceAfter=3,  leftIndent=12, alignment=TA_JUSTIFY)
sBullet   = S("Bullet",  fontSize=10, textColor=BLACK,    leading=15, spaceAfter=2,  leftIndent=20, bulletIndent=10)
sNote     = S("Note",    fontSize=9,  textColor=GRAY,     leading=13, spaceAfter=2,  leftIndent=16)
sCode     = S("Code",    fontSize=9,  textColor=colors.HexColor("#1A237E"), leading=13,
              leftIndent=20, spaceBefore=2, spaceAfter=2, backColor=colors.HexColor("#F3F4FF"))
sTH       = S("TH",      fontSize=9,  textColor=WHITE,    leading=13, alignment=TA_CENTER)
sTD       = S("TD",      fontSize=9,  textColor=BLACK,    leading=13, leftIndent=4)
sTDc      = S("TDc",     fontSize=9,  textColor=BLACK,    leading=13, alignment=TA_CENTER)
sCaption  = S("Caption", fontSize=8,  textColor=GRAY,     leading=11, alignment=TA_CENTER, spaceAfter=6)
sPageNum  = S("PageNum", fontSize=8,  textColor=GRAY,     leading=11, alignment=TA_CENTER)

def hr():     return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CFD8DC"), spaceAfter=6, spaceBefore=4)
def vsp(n=6): return Spacer(1, n)

def h1(txt):
    """섹션 제목 박스"""
    tbl = Table([[Paragraph(txt, sH1)]], colWidths=[W - 40*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return tbl

def h2(txt):  return Paragraph(txt, sH2)
def h3(txt):  return Paragraph(txt, sH3)
def body(txt): return Paragraph(txt, sBody)
def bullet(txt, icon="•"): return Paragraph(f"{icon}  {txt}", sBullet)
def note(txt):  return Paragraph(f"※ {txt}", sNote)
def code(txt):  return Paragraph(txt, sCode)

def info_box(title, lines, bg=BLUE_LT, border=BLUE):
    rows = [[Paragraph(title, S("IBT", fontName=FONT_NAME, fontSize=10, textColor=border, leading=14))]]
    for l in lines:
        rows.append([Paragraph(l, S("IBB", fontName=FONT_NAME, fontSize=9, textColor=BLACK, leading=13, leftIndent=6))])
    tbl = Table(rows, colWidths=[W - 40*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  bg),
        ("BACKGROUND",    (0,1), (-1,-1), colors.white),
        ("BOX",           (0,0), (-1,-1), 1, border),
        ("LINEBELOW",     (0,0), (0,0),   1, border),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    return tbl

def data_table(headers, rows, col_widths=None):
    total = W - 40*mm
    if col_widths is None:
        col_widths = [total / len(headers)] * len(headers)
    data = [[Paragraph(h, sTH) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), sTDc if j == 0 else sTD)
                     for j, c in enumerate(row)])
    tbl = Table(data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("BACKGROUND",    (0,1), (-1,-1), WHITE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GRAY_LT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl

# ── 페이지 번호 콜백 ──────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 15*mm,
        f"SEO JIN PRECISION CO.  |  인사/근태 관리 시스템 사용자 매뉴얼  |  {doc.page} 페이지")
    canvas.restoreState()

# ── 표지 ──────────────────────────────────────────────────────────────────
def cover():
    story = []
    # 상단 컬러 박스
    tbl = Table([[""]], colWidths=[W - 40*mm], rowHeights=[180])
    tbl.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), BLUE)]))
    story.append(tbl)

    # 회사명 + 타이틀을 겹쳐 그리는 방법: 테이블에 넣기
    header_data = [[
        Paragraph("SEO JIN PRECISION CO.", S("Co", fontName=FONT_NAME, fontSize=12, textColor=BLUE_LT, leading=16, alignment=TA_CENTER)),
    ],[
        Paragraph("인사 / 근태 관리 시스템", sTitle),
    ],[
        Paragraph("사용자 매뉴얼", S("MT", fontName=FONT_NAME, fontSize=20, textColor=BLUE_LT, leading=26, alignment=TA_CENTER)),
    ]]
    htbl = Table(header_data, colWidths=[W - 40*mm])
    htbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))

    # 표지 전체를 하나의 테이블로 재구성
    cover_tbl = Table([
        [htbl],
        [Spacer(1, 20)],
        [Paragraph("v 2.0  |  2026년 5월", sSub)],
        [Spacer(1, 40)],
        [Paragraph("이 문서는 SEO JIN PRECISION CO. 인사/근태 관리 시스템의<br/>"
                   "전체 기능과 사용 방법을 상세히 설명합니다.", S("Intro", fontName=FONT_NAME, fontSize=11, textColor=GRAY, leading=18, alignment=TA_CENTER))],
    ], colWidths=[W - 40*mm])
    cover_tbl.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story = [cover_tbl, PageBreak()]
    return story

# ── 목차 ──────────────────────────────────────────────────────────────────
def toc():
    story = [h1("목  차"), vsp(10)]
    entries = [
        ("1", "시스템 개요",                       "3"),
        ("2", "로그인",                             "4"),
        ("3", "대시보드",                           "5"),
        ("4", "인사 관리",                          "6"),
        ("  4.1", "사원 등록",                      "6"),
        ("  4.2", "사원 수정 / 삭제",               "7"),
        ("5", "근태 관리",                          "8"),
        ("  5.1", "출근 / 퇴근 입력",               "8"),
        ("  5.2", "근무시간 자동 계산",             "9"),
        ("  5.3", "컬러 코딩 표시",                "11"),
        ("  5.4", "수동 근태 등록",                "11"),
        ("6", "휴가 관리",                         "12"),
        ("7", "급여 관리",                         "13"),
        ("8", "통계 관리",                         "14"),
        ("9", "자주 묻는 질문 (FAQ)",              "15"),
        ("10", "시스템 요구 사항 및 설치",          "16"),
    ]
    data = []
    for num, title, page in entries:
        indent = 20 if num.startswith("  ") else 4
        data.append([
            Paragraph(num.strip(), S("TN", fontName=FONT_NAME, fontSize=10, textColor=BLUE, leading=14, leftIndent=indent)),
            Paragraph(title,       S("TT", fontName=FONT_NAME, fontSize=10, textColor=BLACK, leading=14, leftIndent=indent)),
            Paragraph(page,        S("TP", fontName=FONT_NAME, fontSize=10, textColor=GRAY,  leading=14, alignment=TA_CENTER)),
        ])
    tbl = Table(data, colWidths=[25*mm, 120*mm, 15*mm])
    tbl.setStyle(TableStyle([
        ("LINEBELOW",     (0,0), (-1,-1), 0.3, colors.HexColor("#E0E0E0")),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [tbl, PageBreak()]
    return story

# ── 1. 시스템 개요 ─────────────────────────────────────────────────────────
def s1_overview():
    story = [h1("1.  시스템 개요"), vsp(8)]
    story += [
        body("SEO JIN PRECISION CO. 인사/근태 관리 시스템은 중소기업의 인사·근태·휴가·급여 업무를 "
             "하나의 프로그램에서 처리할 수 있도록 설계된 데스크탑 애플리케이션입니다."),
        vsp(6),
        h2("1.1  주요 기능"),
    ]
    features = [
        ("대시보드",    "재직 인원, 출근 현황, 휴가 대기, 급여 합계를 한눈에 확인"),
        ("인사 관리",   "사원 등록·수정·삭제, 부서·직급 관리"),
        ("근태 관리",   "출근/퇴근 기록, 근무시간 자동 계산 (정상/초과/야간/특근 구분)"),
        ("휴가 관리",   "연차·병가·휴직 신청, 승인/반려 처리"),
        ("급여 관리",   "기본급 + 각종 수당 - 공제 자동 계산, 월별 급여 처리"),
        ("통계 관리",   "월별 근무유형별 집계 (직원별 정상/초과/야간/특근/야간특근/총 근무시간)"),
    ]
    tbl = Table(
        [[Paragraph(k, S("FK", fontName=FONT_NAME, fontSize=10, textColor=WHITE, leading=13)),
          Paragraph(v, S("FV", fontName=FONT_NAME, fontSize=10, textColor=BLACK, leading=14))]
         for k, v in features],
        colWidths=[35*mm, 120*mm]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), BLUE),
        ("BACKGROUND",    (1,0), (1,-1), WHITE),
        ("ROWBACKGROUNDS",(1,0), (1,-1), [WHITE, GRAY_LT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [tbl, vsp(10)]
    story += [
        h2("1.2  화면 구성"),
        body("프로그램 화면은 <b>헤더(상단)</b>, <b>사이드바(좌측 메뉴)</b>, <b>본문 영역(우측)</b> 세 부분으로 구성됩니다."),
        vsp(4),
    ]
    layout = [
        ["영역", "설명"],
        ["헤더", "회사명, 현재 로그인 사용자, 실시간 시각 표시"],
        ["사이드바", "대시보드 / 인사 / 근태 / 휴가 / 급여 / 통계 메뉴 버튼"],
        ["본문 영역", "선택한 메뉴에 해당하는 화면이 표시되며 스크롤 가능"],
    ]
    story.append(data_table(layout[0], layout[1:], [30*mm, 125*mm]))
    story.append(PageBreak())
    return story

# ── 2. 로그인 ──────────────────────────────────────────────────────────────
def s2_login():
    story = [h1("2.  로그인"), vsp(8)]
    story += [
        body("프로그램을 실행하면 로그인 화면이 나타납니다. 사번과 비밀번호를 입력하여 로그인합니다."),
        vsp(6),
        h2("2.1  로그인 방법"),
        bullet("① 사번(Employee No.) 입력란에 사번을 입력합니다."),
        bullet("② 비밀번호 입력란에 비밀번호를 입력합니다."),
        bullet("③ 'Enter' 키 또는 '로그인' 버튼을 클릭합니다."),
        vsp(6),
    ]
    story.append(info_box("실습 예제 — 관리자 로그인",
        ["사번: ADMIN001", "비밀번호: admin123  (또는 시스템 초기 설정 값)"],
        bg=BLUE_LT, border=BLUE))
    story += [
        vsp(8),
        h2("2.2  기본 계정"),
        data_table(
            ["구분", "사번", "비밀번호", "권한"],
            [["관리자", "ADMIN001", "admin123", "전체 메뉴 접근"],
             ["일반 사원", "사번 입력", "초기: 사번과 동일", "본인 근태만 조회 가능"]],
            [25*mm, 35*mm, 35*mm, 60*mm]
        ),
        vsp(6),
        note("최초 로그인 후 비밀번호를 변경하는 것을 권장합니다."),
    ]
    story.append(PageBreak())
    return story

# ── 3. 대시보드 ────────────────────────────────────────────────────────────
def s3_dashboard():
    story = [h1("3.  대시보드"), vsp(8)]
    story += [
        body("로그인 직후 표시되는 화면입니다. 회사 전체의 주요 지표를 한눈에 파악할 수 있습니다."),
        vsp(6),
        h2("3.1  요약 카드 (4종)"),
    ]
    cards = [
        ["재직 인원", "파란색", "현재 재직 중인 직원 수 (status = '재직')"],
        ["오늘 출근", "청록색", "오늘 날짜 기준 출근 기록이 있는 직원 수"],
        ["휴가 대기", "주황색", "승인 대기 중인 휴가 신청 건수"],
        ["이번 달 급여", "보라색", "당월 처리된 순수령액 합계"],
    ]
    story.append(data_table(["카드명", "색상", "표시 내용"], cards, [30*mm, 25*mm, 100*mm]))
    story += [
        vsp(8),
        h2("3.2  부서별 인원 현황"),
        body("재직 중인 직원을 부서별로 집계하여 표로 보여 줍니다."),
        vsp(6),
        h2("3.3  휴가 신청 대기 목록"),
        body("승인 대기 중인 휴가 신청 내역을 최신 순으로 표시합니다."),
        note("건수가 많을 경우 우측 스크롤바를 이용해 아래 내용을 확인하세요."),
    ]
    story.append(PageBreak())
    return story

# ── 4. 인사 관리 ───────────────────────────────────────────────────────────
def s4_employees():
    story = [h1("4.  인사 관리"), vsp(8)]
    story += [
        body("좌측 메뉴에서 '👤 인사 관리'를 클릭하면 사원 기본 정보 관리 화면으로 이동합니다."),
        vsp(8),
        h2("4.1  사원 등록"),
        bullet("① 상단 입력 폼에 사원 정보를 입력합니다."),
        bullet("② 필수 항목: 사번(*), 이름(*)"),
        bullet("③ '저장' 버튼을 클릭하면 DB에 등록됩니다."),
        vsp(6),
    ]
    story.append(info_box("실습 예제 — 사원 등록",
        ["사번: EMP006",
         "이름: 홍길동",
         "부서: 생산팀",
         "직급: 사원",
         "입사일: 2026-05-01",
         "기본급: 3,000,000",
         "→ 입력 후 [저장] 클릭 → 하단 목록에 추가 확인"],
        bg=BLUE_LT, border=BLUE))
    story += [
        vsp(8),
        h2("4.2  사원 수정"),
        bullet("① 하단 목록에서 수정할 사원 행을 클릭합니다."),
        bullet("② 상단 입력 폼에 정보가 자동으로 채워집니다."),
        bullet("③ 원하는 항목을 수정 후 '저장'을 클릭합니다."),
        vsp(6),
        h2("4.3  사원 삭제"),
        bullet("① 목록에서 삭제할 사원을 클릭합니다."),
        bullet("② '삭제' 버튼 클릭 → 확인 대화상자 → 'OK'를 클릭합니다."),
        note("삭제된 사원의 근태·급여 데이터는 유지되나 사원 목록에서는 제거됩니다."),
        vsp(8),
        h2("4.4  입력 필드 설명"),
        data_table(
            ["필드명", "필수", "설명"],
            [["사번",     "○", "고유 직원 번호 (중복 불가)"],
             ["이름",     "○", "한글 또는 영문 이름"],
             ["부서",     "",  "생산팀 / 품질팀 / 경영지원 / 영업팀 / 연구개발 / 품질관리"],
             ["직급",     "",  "사원 / 대리 / 과장 / 차장 / 부장 / 이사"],
             ["입사일",   "",  "YYYY-MM-DD 형식"],
             ["전화번호", "",  "010-XXXX-XXXX"],
             ["이메일",   "",  "이메일 주소"],
             ["기본급",   "",  "세전 월 기본급 (원)"],
             ["재직상태", "",  "재직 / 휴직 / 퇴직"]],
            [25*mm, 15*mm, 115*mm]
        ),
    ]
    story.append(PageBreak())
    return story

# ── 5. 근태 관리 ───────────────────────────────────────────────────────────
def s5_attendance():
    story = [h1("5.  근태 관리"), vsp(8)]
    story += [
        body("'⏱ 근태 관리' 메뉴에서 직원의 출퇴근 기록을 관리하고 근무시간을 자동으로 계산합니다."),
        vsp(8),
        h2("5.1  출근 / 퇴근 입력"),
        bullet("① 상단 폼에서 사원 선택, 날짜, 출근 시각, 퇴근 시각을 입력합니다."),
        bullet("② '출근 처리' 버튼을 클릭하면 출근이 기록됩니다."),
        bullet("③ 퇴근 시각을 입력 후 '퇴근 처리'를 클릭하면 근무시간이 자동 계산됩니다."),
        vsp(6),
        info_box("실습 예제 — 평일 야근",
            ["사원: 홍길동 (EMP006)",
             "날짜: 2026-05-20 (화)",
             "출근: 08:30  /  퇴근: 21:00",
             "→ 정상근무 8.0h  |  초과근무 3.0h  (17:30~21:00, 0.5h 공제)"],
            bg=BLUE_LT, border=BLUE),
        vsp(10),
    ]

    story += [h2("5.2  근무시간 자동 계산 규칙"), vsp(4)]

    # 근무 구간 표
    story.append(data_table(
        ["근무 구분", "시간 구간", "휴게 공제", "비고"],
        [["정상근무",  "08:30 ~ 17:30", "1시간 (근무 > 4h)", "주중 최대 8.0h"],
         ["초과근무",  "17:30 ~ 22:00", "0.5시간 (근무 > 4h)", "주중 최대 4.0h"],
         ["야간근무",  "22:00 ~ 05:30", "없음",              "공제 없이 전액 인정"],
         ["특근",      "08:30 ~ 22:00 (주말/공휴일)", "1시간", ""],
         ["야간특근",  "22:00 ~ 05:30 (주말/공휴일)", "없음",  "메모에 '야간특근' 자동 기재"]],
        [30*mm, 45*mm, 30*mm, 50*mm]
    ))

    story += [
        vsp(10),
        h3("계산 예제 ① — 평일 정상 근무"),
        code("출근 08:30  /  퇴근 17:30"),
        code("정상근무 = 9.0h - 1.0h(휴게) = 8.0h  |  초과 = 0  |  야간 = 0"),
        vsp(4),
        h3("계산 예제 ② — 평일 야근 포함"),
        code("출근 08:30  /  퇴근 21:00"),
        code("정상근무: 08:30~17:30 → 9.0h - 1.0h = 8.0h"),
        code("초과근무: 17:30~21:00 → 3.5h - 0.5h = 3.0h"),
        code("야간근무: 0  (22:00 이전 퇴근)"),
        vsp(4),
        h3("계산 예제 ③ — 심야 근무 (22시 이후)"),
        code("출근 20:00  /  퇴근 다음날 02:00"),
        code("초과근무: 20:00~22:00 → 2.0h (0.5h 미만이므로 공제 없음)"),
        code("야간근무: 22:00~02:00 → 4.0h (공제 없음)"),
        vsp(4),
        h3("계산 예제 ④ — 토요일 특근"),
        code("날짜: 2026-05-23 (토)  /  출근 09:00  /  퇴근 18:00"),
        code("특근: 09:00~18:00 → 9.0h - 1.0h = 8.0h"),
        code("야간특근: 0  (22:00 이전 퇴근)"),
        vsp(4),
        h3("계산 예제 ⑤ — 공휴일 야간특근"),
        code("날짜: 2026-06-06 (현충일)  /  출근 23:00  /  퇴근 다음날 04:00"),
        code("야간특근: 23:00~04:00 → 5.0h (공제 없음)"),
        code("→ 메모란에 '야간특근' 자동 기재"),
        vsp(8),
    ]

    story += [
        h2("5.3  컬러 코딩 표시"),
        body("근태 목록 테이블에서 각 근무 유형은 이모지로 구분되어 표시됩니다."),
        vsp(4),
        data_table(
            ["이모지", "근무 유형", "설명"],
            [["(흰색)", "정상근무", "08:30 ~ 17:30 구간 근무시간"],
             ["🟠", "초과근무",   "17:30 ~ 22:00 구간 연장 근무"],
             ["🔵", "야간근무",   "22:00 ~ 05:30 구간 야간 근무"],
             ["🔴", "특근",       "주말/공휴일 근무 (야간특근 포함)"]],
            [15*mm, 30*mm, 110*mm]
        ),
        vsp(8),
        h2("5.4  수동 근태 등록 및 수정"),
        bullet("① 수정할 근태 행을 클릭하면 상단 폼에 자동 입력됩니다."),
        bullet("② 시각이나 메모를 수정 후 '수정' 버튼을 클릭합니다."),
        bullet("③ '결근'으로 상태를 변경하면 해당일 근무시간은 0으로 처리됩니다."),
        note("결근 처리된 날은 통계에서 제외됩니다."),
    ]
    story.append(PageBreak())
    return story

# ── 6. 휴가 관리 ───────────────────────────────────────────────────────────
def s6_leaves():
    story = [h1("6.  휴가 관리"), vsp(8)]
    story += [
        body("'🌴 휴가 관리' 메뉴에서 직원의 연차·병가·휴직 신청 및 승인을 처리합니다."),
        vsp(8),
        h2("6.1  휴가 신청"),
        bullet("① 상단 폼에서 사원, 휴가 유형, 시작일, 종료일, 사유를 입력합니다."),
        bullet("② '저장' 버튼 클릭 → 신청 상태 '대기'로 등록됩니다."),
        vsp(6),
        info_box("실습 예제 — 연차 신청",
            ["사원: 홍길동  |  구분: 연차",
             "시작일: 2026-06-02  |  종료일: 2026-06-03",
             "일수: 2일  |  사유: 개인 사정",
             "→ [저장] 클릭 → 상태 '대기'로 목록에 추가"],
            bg=BLUE_LT, border=BLUE),
        vsp(8),
        h2("6.2  승인 / 반려"),
        bullet("① 목록에서 처리할 휴가 신청 행을 클릭합니다."),
        bullet("② '승인' 또는 '반려' 버튼을 클릭합니다."),
        bullet("③ 처리 결과가 목록에 즉시 반영됩니다."),
        vsp(8),
        h2("6.3  휴가 유형"),
        data_table(
            ["유형", "설명"],
            [["연차",   "근로기준법에 따른 연차 유급휴가"],
             ["병가",   "질병·부상으로 인한 휴가"],
             ["휴직",   "장기 휴직 (육아휴직, 개인 사유 등)"],
             ["기타",   "상기 외 기타 사유"]],
            [30*mm, 125*mm]
        ),
        note("일수는 시작일~종료일 사이의 실제 일수를 직접 입력합니다 (주말 제외 여부는 수동 확인)."),
    ]
    story.append(PageBreak())
    return story

# ── 7. 급여 관리 ───────────────────────────────────────────────────────────
def s7_payroll():
    story = [h1("7.  급여 관리"), vsp(8)]
    story += [
        body("'💰 급여 관리' 메뉴에서 월별 급여를 계산하고 관리합니다."),
        vsp(8),
        h2("7.1  급여 계산 구조"),
    ]
    story.append(data_table(
        ["항목", "구분", "설명"],
        [["기본급",        "지급", "사원 마스터에 등록된 월 기본급"],
         ["초과수당",      "지급", "초과근무시간 × 시간급 × 1.5"],
         ["야간수당",      "지급", "야간근무시간 × 시간급 × 0.5"],
         ["특근수당",      "지급", "특근시간 × 시간급 × 1.5"],
         ["야간특근수당",  "지급", "야간특근시간 × 시간급 × 2.0"],
         ["공제",          "차감", "4대보험, 소득세 등 (직접 입력)"],
         ["순수령액",      "합계", "= 기본급 + 수당 합계 - 공제"]],
        [35*mm, 20*mm, 100*mm]
    ))
    story += [
        vsp(8),
        h2("7.2  급여 처리 방법"),
        bullet("① 상단에서 지급 월(YYYY-MM)을 선택합니다."),
        bullet("② 사원을 선택하면 해당 월 근태 데이터를 기반으로 수당이 자동 계산됩니다."),
        bullet("③ 공제 항목을 직접 입력합니다."),
        bullet("④ '저장' 클릭 → 해당 사원의 월 급여가 저장됩니다."),
        vsp(6),
        info_box("실습 예제 — 2026년 5월 급여 처리",
            ["사원: 홍길동  |  지급월: 2026-05",
             "기본급: 3,000,000  |  초과근무 10h: +225,000",
             "야간근무 5h: +56,250  |  공제: 350,000",
             "→ 순수령액 = 3,000,000 + 281,250 - 350,000 = 2,931,250원"],
            bg=BLUE_LT, border=BLUE),
        note("시간급 = 기본급 ÷ 209 (통상임금 산정 기준)"),
    ]
    story.append(PageBreak())
    return story

# ── 8. 통계 관리 ───────────────────────────────────────────────────────────
def s8_stats():
    story = [h1("8.  통계 관리"), vsp(8)]
    story += [
        body("'📊 통계 관리' 메뉴에서 월별 직원별 근무시간 집계를 확인합니다."),
        vsp(8),
        h2("8.1  화면 구성"),
        bullet("상단 '◀ 이전달  /  다음달 ▶' 버튼으로 조회 월을 변경합니다."),
        bullet("표에는 해당 월에 근태 기록이 있는 모든 직원이 표시됩니다."),
        vsp(6),
        h2("8.2  집계 항목"),
        data_table(
            ["컬럼명", "설명"],
            [["사번",      "직원 고유 번호"],
             ["이름",      "직원 이름"],
             ["정상근무",  "해당 월 정상근무 시간 합계 (결근 제외)"],
             ["초과근무",  "해당 월 초과근무 시간 합계"],
             ["야간근무",  "해당 월 야간근무 시간 합계 (야간특근 제외)"],
             ["특근",      "해당 월 특근 시간 합계"],
             ["야간특근",  "해당 월 야간특근 시간 합계 (메모에 '야간특근' 포함된 건)"],
             ["총 근무시간","정상 + 초과 + 야간 + 특근 + 야간특근 합계"]],
            [30*mm, 125*mm]
        ),
        vsp(8),
        info_box("실습 예제 — 2026년 5월 통계 조회",
            ["→ 상단 월 선택: 2026-05",
             "→ 홍길동: 정상 160.0h / 초과 15.0h / 야간 8.0h / 특근 16.0h / 총 199.0h",
             "※ 결근 처리된 날은 모든 항목에서 제외됩니다."],
            bg=BLUE_LT, border=BLUE),
        note("통계 데이터는 근태 관리 메뉴에서 입력된 실제 데이터를 집계한 것입니다."),
    ]
    story.append(PageBreak())
    return story

# ── 9. FAQ ────────────────────────────────────────────────────────────────
def s9_faq():
    story = [h1("9.  자주 묻는 질문 (FAQ)"), vsp(8)]
    faqs = [
        ("Q. 퇴근 시각이 자정을 넘으면 어떻게 입력하나요?",
         "퇴근 시각을 '다음날 시각'으로 처리합니다. 시스템이 출근 시각보다 퇴근 시각이 "
         "작으면 자동으로 +24시간 처리하여 야간 근무시간을 올바르게 계산합니다."),
        ("Q. 휴일이 달력에 없어 자동 인식이 안 될 때는?",
         "근태 입력 시 메모란에 '특근' 또는 '야간특근'을 직접 입력하면 급여 계산 시 "
         "해당 수당으로 처리됩니다. 또한 개발자에게 공휴일 목록 업데이트를 요청하세요."),
        ("Q. 사원을 실수로 삭제했습니다. 복구할 수 있나요?",
         "삭제된 사원은 복구가 불가능합니다. 평소 hr.db 파일을 정기적으로 백업하세요. "
         "백업 파일이 있다면 해당 파일로 교체하여 데이터를 복구할 수 있습니다."),
        ("Q. 근무시간 계산이 잘못된 것 같습니다.",
         "근태 목록에서 해당 행을 클릭하여 출/퇴근 시각을 확인하세요. 시각이 올바르면 "
         "'수정' 버튼으로 데이터를 갱신하면 자동으로 재계산됩니다."),
        ("Q. 통계 페이지에 일부 직원이 표시되지 않습니다.",
         "해당 월에 근태 기록이 없는 직원은 통계에 표시되지 않습니다. "
         "근태 관리에서 해당 직원의 해당 월 기록을 확인하세요."),
        ("Q. 프로그램이 느리거나 응답이 없습니다.",
         "hr.db 파일의 데이터가 매우 많을 경우 느려질 수 있습니다. "
         "프로그램을 재시작하거나 불필요한 근태 데이터를 정리하세요."),
    ]
    for q, a in faqs:
        story += [
            KeepTogether([
                Paragraph(q, S("Q", fontName=FONT_NAME, fontSize=10, textColor=BLUE, leading=15,
                               spaceBefore=8, spaceAfter=2, leftIndent=8)),
                Paragraph(a, S("A", fontName=FONT_NAME, fontSize=10, textColor=BLACK, leading=15,
                               spaceAfter=4, leftIndent=20)),
                hr(),
            ])
        ]
    story.append(PageBreak())
    return story

# ── 10. 설치 및 요구 사항 ─────────────────────────────────────────────────
def s10_install():
    story = [h1("10.  시스템 요구 사항 및 설치"), vsp(8)]
    story += [
        h2("10.1  시스템 요구 사항"),
        data_table(
            ["항목", "최소", "권장"],
            [["운영체제", "Windows 10 (64-bit)", "Windows 11 (64-bit)"],
             ["CPU",     "Intel Core i3",        "Intel Core i5 이상"],
             ["메모리",  "4 GB RAM",             "8 GB RAM 이상"],
             ["저장공간","100 MB 여유 공간",      "500 MB 이상"],
             ["화면 해상도", "1280 × 768",        "1920 × 1080 이상"]],
            [30*mm, 60*mm, 65*mm]
        ),
        vsp(10),
        h2("10.2  설치 방법"),
        bullet("① GitHub 저장소 또는 배포처에서 SEOJIN_HR.exe 파일을 다운로드합니다."),
        bullet("② 다운로드한 EXE 파일을 원하는 폴더에 복사합니다."),
        bullet("③ SEOJIN_HR.exe를 더블클릭하여 실행합니다."),
        bullet("④ 처음 실행 시 동일 폴더에 hr.db(데이터베이스) 파일이 자동 생성됩니다."),
        note("설치 프로그램이 없으므로 EXE 파일만 있으면 즉시 사용 가능합니다."),
        vsp(8),
        h2("10.3  데이터 백업"),
        bullet("데이터는 EXE와 같은 폴더의 <b>hr.db</b> 파일에 저장됩니다."),
        bullet("정기적으로 hr.db 파일을 별도 위치에 복사하여 백업하세요."),
        bullet("복구 시 hr.db 파일을 EXE와 같은 폴더에 덮어쓰기 하면 됩니다."),
        vsp(8),
        h2("10.4  GitHub 저장소"),
        body("소스 코드 및 최신 릴리스는 아래 주소에서 확인할 수 있습니다."),
        code("https://github.com/kuiseob/hr-attendance"),
        vsp(6),
        note("문의 사항은 GitHub Issues를 통해 등록해 주세요."),
    ]
    return story

# ── 메인 ──────────────────────────────────────────────────────────────────
def build_pdf(out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm,  bottomMargin=20*mm,
        title="SEO JIN HR 사용자 매뉴얼",
        author="SEO JIN PRECISION CO.",
    )
    story = []
    story += cover()
    story += toc()
    story += s1_overview()
    story += s2_login()
    story += s3_dashboard()
    story += s4_employees()
    story += s5_attendance()
    story += s6_leaves()
    story += s7_payroll()
    story += s8_stats()
    story += s9_faq()
    story += s10_install()
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF 생성 완료: {out_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SEOJIN_HR_사용자매뉴얼.pdf")
    build_pdf(out)
