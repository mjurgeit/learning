"""Generates the three freelancer workbooks (blank + DEMO versions). Run: python3 make_xlsx.py"""
import datetime as dt, os, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter as L

OUT = os.path.join(os.path.dirname(__file__), "..", "products")
NAVY, TEAL, LIGHT, INPUT = "1F2A44", "2A9D8F", "EAF4F3", "FFF8E1"
hfont = Font(bold=True, color="FFFFFF", name="Calibri")
hfill = PatternFill("solid", fgColor=NAVY)
tfill = PatternFill("solid", fgColor=TEAL)
lfill = PatternFill("solid", fgColor=LIGHT)
ifill = PatternFill("solid", fgColor=INPUT)
thin = Side(style="thin", color="CCCCCC")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
MONEY = '$#,##0.00;[Red]-$#,##0.00'
DATE = "yyyy-mm-dd"
N = 500  # data rows

def header(ws, row, labels, widths=None):
    for i, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=t)
        c.font, c.fill, c.border = hfont, hfill, box
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if widths: ws.column_dimensions[L(i)].width = widths[i-1]
    ws.row_dimensions[row].height = 30
    ws.freeze_panes = ws.cell(row=row+1, column=1)

def title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = Font(bold=True, size=16, color=NAVY)
    if sub: ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="666666")

def style_inputs(ws, r1, r2, cols):
    for r in range(r1, r2+1):
        for c in cols:
            ws.cell(row=r, column=c).fill = ifill; ws.cell(row=r, column=c).border = box

CATS = ["Software & Subscriptions","Equipment & Hardware","Home Office","Internet & Phone","Marketing & Advertising",
        "Professional Services","Education & Training","Travel","Meals (50%)","Contractors & Subcontractors",
        "Bank & Payment Fees","Insurance","Office Supplies","Other"]

# ---------------------------------------------------------------- WORKBOOK 1
def build_finance(demo):
    wb = Workbook()
    # ---- Settings
    S = wb.active; S.title = "Settings"
    title(S, "Settings", "Yellow cells are yours to edit. Everything else calculates.")
    rows = [("Tax year", 2026, "0"),
            ("Self-employment tax rate", 0.153, "0.0%"),
            ("Net earnings factor (SE base)", 0.9235, "0.00%"),
            ("Est. income tax rate on profit", 0.12, "0.0%"),
            ("State / local tax rate on profit", 0.04, "0.0%"),
            ("Extra cushion on tax set-aside", 0.05, "0.0%")]
    for i, (k, v, f) in enumerate(rows, 4):
        S.cell(row=i, column=1, value=k); c = S.cell(row=i, column=2, value=v); c.number_format = f; c.fill = ifill; c.border = box
    S["A11"] = "Estimated-tax payment due dates (edit if the IRS shifts them)"; S["A11"].font = Font(bold=True)
    dues = [("Period 1 (Jan-Mar)", dt.date(2026,4,15)), ("Period 2 (Apr-May)", dt.date(2026,6,15)),
            ("Period 3 (Jun-Aug)", dt.date(2026,9,15)), ("Period 4 (Sep-Dec)", dt.date(2027,1,18))]
    for i, (k, v) in enumerate(dues, 12):
        S.cell(row=i, column=1, value=k); c = S.cell(row=i, column=2, value=v); c.number_format = DATE; c.fill = ifill; c.border = box
    S["A17"] = "Expense categories (edit the list; dropdown on Expenses uses it)"; S["A17"].font = Font(bold=True)
    for i, c_ in enumerate(CATS, 18):
        c = S.cell(row=i, column=1, value=c_); c.fill = ifill; c.border = box
    S["D4"] = "Notes"; S["D4"].font = Font(bold=True)
    notes = ["Tax periods follow the IRS estimated-tax schedule, not calendar quarters:",
             "P1 Jan-Mar, P2 Apr-May, P3 Jun-Aug, P4 Sep-Dec.",
             "Default rates are placeholders - set them with your accountant or IRS Form 1040-ES.",
             "This workbook gives estimates for planning. It is not tax advice."]
    for i, n in enumerate(notes, 5): S.cell(row=i, column=4, value=n)
    S.column_dimensions["A"].width = 44; S.column_dimensions["B"].width = 14; S.column_dimensions["D"].width = 70
    S.cell(row=12, column=1).number_format = "General"

    # ---- Income
    I = wb.create_sheet("Income")
    header(I, 4, ["Date received","Client","Invoice #","Description","Amount","Payment method","Year","Tax period","Month"],
           [14,24,12,34,14,16,8,10,8])
    title(I, "Income log", "One row per payment received. Put the Invoice # to auto-reconcile the Invoices sheet.")
    for r in range(5, 5+N):
        I.cell(row=r, column=7, value=f'=IF(A{r}="","",YEAR(A{r}))')
        I.cell(row=r, column=8, value=f'=IF(A{r}="","",IF(MONTH(A{r})<=3,1,IF(MONTH(A{r})<=5,2,IF(MONTH(A{r})<=8,3,4))))')
        I.cell(row=r, column=9, value=f'=IF(A{r}="","",MONTH(A{r}))')
        I.cell(row=r, column=1).number_format = DATE; I.cell(row=r, column=5).number_format = MONEY
    style_inputs(I, 5, 4+N, range(1, 7))
    dv = DataValidation(type="list", formula1='"Bank transfer,PayPal,Stripe,Wise,Check,Cash,Other"', allow_blank=True)
    I.add_data_validation(dv); dv.add(f"F5:F{4+N}")

    # ---- Expenses
    E = wb.create_sheet("Expenses")
    title(E, "Expense log", "Deductible % lets you log partial-use items (phone 50%, meals 50%). Leave blank for 100%.")
    header(E, 4, ["Date","Vendor","Category","Description","Amount paid","Deductible %","Deductible amount","Year","Tax period","Month"],
           [14,22,26,32,14,12,16,8,10,8])
    for r in range(5, 5+N):
        E.cell(row=r, column=7, value=f'=IF(OR(A{r}="",E{r}=""),"",E{r}*IF(F{r}="",1,F{r}))')
        E.cell(row=r, column=8, value=f'=IF(A{r}="","",YEAR(A{r}))')
        E.cell(row=r, column=9, value=f'=IF(A{r}="","",IF(MONTH(A{r})<=3,1,IF(MONTH(A{r})<=5,2,IF(MONTH(A{r})<=8,3,4))))')
        E.cell(row=r, column=10, value=f'=IF(A{r}="","",MONTH(A{r}))')
        E.cell(row=r, column=1).number_format = DATE
        E.cell(row=r, column=5).number_format = MONEY; E.cell(row=r, column=7).number_format = MONEY
        E.cell(row=r, column=6).number_format = "0%"
    style_inputs(E, 5, 4+N, range(1, 7))
    dv2 = DataValidation(type="list", formula1="=Settings!$A$18:$A$31", allow_blank=True)
    E.add_data_validation(dv2); dv2.add(f"C5:C{4+N}")

    # ---- Invoices
    V = wb.create_sheet("Invoices")
    title(V, "Invoice tracker", "Enter the invoice details. Paid amount fills itself from the Income log (matched by Invoice #).")
    header(V, 4, ["Invoice #","Client","Issue date","Terms (days)","Due date","Amount","Paid to date","Balance","Status","Days overdue"],
           [12,24,13,12,13,14,14,14,12,12])
    for r in range(5, 5+N):
        V.cell(row=r, column=5, value=f'=IF(OR(C{r}="",D{r}=""),"",C{r}+D{r})')
        V.cell(row=r, column=7, value=f'=IF(A{r}="","",SUMIFS(Income!$E$5:$E${4+N},Income!$C$5:$C${4+N},A{r}))')
        V.cell(row=r, column=8, value=f'=IF(OR(A{r}="",F{r}=""),"",F{r}-G{r})')
        V.cell(row=r, column=9, value=f'=IF(OR(A{r}="",F{r}=""),"",IF(H{r}<=0.004,"Paid",IF(AND(E{r}<>"",TODAY()>E{r}),"Overdue",IF(G{r}>0,"Partial","Open"))))')
        V.cell(row=r, column=10, value=f'=IF(I{r}="Overdue",TODAY()-E{r},"")')
        V.cell(row=r, column=3).number_format = DATE; V.cell(row=r, column=5).number_format = DATE
        for c in (6, 7, 8): V.cell(row=r, column=c).number_format = MONEY
    style_inputs(V, 5, 4+N, [1, 2, 3, 4, 6])
    V.conditional_formatting.add(f"I5:I{4+N}", CellIsRule(operator="equal", formula=['"Overdue"'], fill=PatternFill("solid", bgColor="F8CBAD", fgColor="F8CBAD")))
    V.conditional_formatting.add(f"I5:I{4+N}", CellIsRule(operator="equal", formula=['"Paid"'], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))

    # ---- Clients
    C = wb.create_sheet("Clients")
    title(C, "Client summary", "Type client names in column A (exactly as in Income/Invoices). Totals are for the tax year in Settings.")
    header(C, 4, ["Client","Invoiced","Received","Outstanding","% of income","Invoices"], [28,16,16,16,12,10])
    for r in range(5, 35):
        C.cell(row=r, column=2, value=f'=IF(A{r}="","",SUMIFS(Invoices!$F$5:$F${4+N},Invoices!$B$5:$B${4+N},A{r},Invoices!$C$5:$C${4+N},">="&DATE(Settings!$B$4,1,1),Invoices!$C$5:$C${4+N},"<="&DATE(Settings!$B$4,12,31)))')
        C.cell(row=r, column=3, value=f'=IF(A{r}="","",SUMIFS(Income!$E$5:$E${4+N},Income!$B$5:$B${4+N},A{r},Income!$G$5:$G${4+N},Settings!$B$4))')
        C.cell(row=r, column=4, value=f'=IF(A{r}="","",SUMIFS(Invoices!$H$5:$H${4+N},Invoices!$B$5:$B${4+N},A{r}))')
        C.cell(row=r, column=5, value=f'=IF(OR(A{r}="",SUM($C$5:$C$34)=0),"",C{r}/SUM($C$5:$C$34))')
        C.cell(row=r, column=6, value=f'=IF(A{r}="","",COUNTIFS(Invoices!$B$5:$B${4+N},A{r}))')
        for c in (2, 3, 4): C.cell(row=r, column=c).number_format = MONEY
        C.cell(row=r, column=5).number_format = "0.0%"
    style_inputs(C, 5, 34, [1])

    # ---- Tax
    T = wb.create_sheet("Tax Estimator")
    title(T, "Estimated tax set-aside", "Per IRS payment period for the tax year in Settings. Planning estimate only.")
    header(T, 4, ["Period","Due date","Income","Deductible expenses","Net profit","SE tax","Income + state tax","Total to set aside","Cumulative set-aside"],
           [22,13,15,18,15,14,18,18,18])
    labels = ["P1 Jan-Mar","P2 Apr-May","P3 Jun-Aug","P4 Sep-Dec"]
    for k in range(4):
        r = 5+k
        T.cell(row=r, column=1, value=labels[k])
        T.cell(row=r, column=2, value=f"=Settings!B{12+k}").number_format = DATE
        T.cell(row=r, column=3, value=f'=SUMIFS(Income!$E$5:$E${4+N},Income!$H$5:$H${4+N},{k+1},Income!$G$5:$G${4+N},Settings!$B$4)')
        T.cell(row=r, column=4, value=f'=SUMIFS(Expenses!$G$5:$G${4+N},Expenses!$I$5:$I${4+N},{k+1},Expenses!$H$5:$H${4+N},Settings!$B$4)')
        T.cell(row=r, column=5, value=f"=C{r}-D{r}")
        T.cell(row=r, column=6, value=f"=MAX(0,E{r})*Settings!$B$6*Settings!$B$5")
        T.cell(row=r, column=7, value=f"=MAX(0,E{r}-F{r}/2)*(Settings!$B$7+Settings!$B$8)")
        T.cell(row=r, column=8, value=f"=(F{r}+G{r})*(1+Settings!$B$9)")
        T.cell(row=r, column=9, value=f"=SUM($H$5:H{r})")
        for c in range(3, 10): T.cell(row=r, column=c).number_format = MONEY
    T["A9"] = "Year total"; T["A9"].font = Font(bold=True)
    for c in range(3, 9):
        T.cell(row=9, column=c, value=f"=SUM({L(c)}5:{L(c)}8)").number_format = MONEY
        T.cell(row=9, column=c).font = Font(bold=True)
    T["A11"] = "How it works: SE tax = net profit x 92.35% x 15.3%. Income tax = (profit - half of SE tax) x your income + state rates. Then your cushion is added."
    T["A12"] = "Move the 'Total to set aside' amount into a separate savings account the week each payment lands."

    # ---- Dashboard
    D = wb.create_sheet("Dashboard", 0)
    title(D, "Freelancer Finance Dashboard")
    D["A2"] = '="Tax year "&Settings!B4&"  |  updated "&TEXT(TODAY(),"yyyy-mm-dd")'
    D["A2"].font = Font(italic=True, color="666666")
    kp = [("Income (YTD)", f'=SUMIFS(Income!$E$5:$E${4+N},Income!$G$5:$G${4+N},Settings!$B$4)', MONEY),
          ("Deductible expenses", f'=SUMIFS(Expenses!$G$5:$G${4+N},Expenses!$H$5:$H${4+N},Settings!$B$4)', MONEY),
          ("Net profit", "=B4-B5", MONEY),
          ("Profit margin", '=IF(B4=0,0,B6/B4)', "0.0%"),
          ("Tax to set aside (est.)", "='Tax Estimator'!H9", MONEY),
          ("Take-home after tax (est.)", "=B6-B8", MONEY),
          ("Outstanding invoices", f'=SUM(Invoices!$H$5:$H${4+N})', MONEY),
          ("Overdue amount", f'=SUMIFS(Invoices!$H$5:$H${4+N},Invoices!$I$5:$I${4+N},"Overdue")', MONEY),
          ("Overdue invoices (count)", f'=COUNTIFS(Invoices!$I$5:$I${4+N},"Overdue")', "0"),
          ("Top client share of income", "=IF(SUM(Clients!C5:C34)=0,0,MAX(Clients!E5:E34))", "0.0%")]
    for i, (k, f, nf) in enumerate(kp, 4):
        a = D.cell(row=i, column=1, value=k); a.font = Font(bold=True); a.fill = lfill; a.border = box
        b = D.cell(row=i, column=2, value=f); b.number_format = nf; b.border = box; b.font = Font(bold=True, color=NAVY, size=12)
    D.column_dimensions["A"].width = 30; D.column_dimensions["B"].width = 18
    D["D3"] = "Month"; D["E3"] = "Income"; D["F3"] = "Expenses"; D["G3"] = "Profit"
    for c in "DEFG": D[f"{c}3"].font = hfont; D[f"{c}3"].fill = hfill
    mn = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for m in range(12):
        r = 4+m
        D.cell(row=r, column=4, value=mn[m])
        D.cell(row=r, column=5, value=f'=SUMIFS(Income!$E$5:$E${4+N},Income!$I$5:$I${4+N},{m+1},Income!$G$5:$G${4+N},Settings!$B$4)')
        D.cell(row=r, column=6, value=f'=SUMIFS(Expenses!$G$5:$G${4+N},Expenses!$J$5:$J${4+N},{m+1},Expenses!$H$5:$H${4+N},Settings!$B$4)')
        D.cell(row=r, column=7, value=f"=E{r}-F{r}")
        for c in (5, 6, 7): D.cell(row=r, column=c).number_format = MONEY
    D["D16"] = "Total"; D["D16"].font = Font(bold=True)
    for c in "EFG": D[f"{c}16"] = f"=SUM({c}4:{c}15)"; D[f"{c}16"].number_format = MONEY; D[f"{c}16"].font = Font(bold=True)
    for c, w in zip("DEFG", (10, 14, 14, 14)): D.column_dimensions[c].width = w
    D["A16"] = "Spending by category"; D["A16"].font = Font(bold=True, color=NAVY)
    D["A17"] = "Category"; D["B17"] = "Deductible $"
    for c in "AB": D[f"{c}17"].font = hfont; D[f"{c}17"].fill = hfill
    for i in range(14):
        r = 18+i
        D.cell(row=r, column=1, value=f"=Settings!A{18+i}")
        D.cell(row=r, column=2, value=f'=SUMIFS(Expenses!$G$5:$G${4+N},Expenses!$C$5:$C${4+N},A{r},Expenses!$H$5:$H${4+N},Settings!$B$4)').number_format = MONEY
    ch = BarChart(); ch.type = "col"; ch.title = "Income vs expenses by month"; ch.height = 8; ch.width = 18
    ch.add_data(Reference(D, min_col=5, max_col=6, min_row=3, max_row=15), titles_from_data=True)
    ch.set_categories(Reference(D, min_col=4, min_row=4, max_row=15))
    D.add_chart(ch, "I3")
    pc = PieChart(); pc.title = "Expenses by category"; pc.height = 8; pc.width = 12
    pc.add_data(Reference(D, min_col=2, min_row=17, max_row=31), titles_from_data=True)
    pc.set_categories(Reference(D, min_col=1, min_row=18, max_row=31))
    D.add_chart(pc, "I20")

    # ---- Start Here
    H = wb.create_sheet("Start Here", 0)
    title(H, "Freelancer Finance Tracker - Start Here")
    steps = ["1. Settings: set your tax year, tax rates and due dates (yellow cells).",
             "2. Invoices: log each invoice you send (number, client, date, terms, amount).",
             "3. Income: log every payment you receive. Enter the Invoice # and the invoice marks itself Paid / Partial.",
             "4. Expenses: log business costs; pick a category; use Deductible % for partly personal items.",
             "5. Clients: type your client names in column A to see who pays you and who owes you.",
             "6. Dashboard + Tax Estimator update automatically. Move the 'tax to set aside' into savings.",
             "",
             "Yellow = you type. White = formulas, do not overwrite. Rows 5-504 on each log are pre-built.",
             "Google Sheets: File > Import > Upload > 'Replace spreadsheet'. Formulas and dropdowns carry over.",
             "Disclaimer: planning tool, not tax or legal advice. Check rates at irs.gov or with a tax professional."]
    for i, s in enumerate(steps, 3): H.cell(row=i, column=1, value=s)
    H.column_dimensions["A"].width = 120

    if demo:
        d = dt.date
        inc = [(d(2026,1,20),"Acme Co","INV-001","Brand design",2500,"Bank transfer"),
               (d(2026,2,18),"Acme Co","INV-002","Landing page",1800,"Stripe"),
               (d(2026,4,10),"Birch Studio","INV-003","Copywriting",1200,"PayPal"),
               (d(2026,5,20),"Cobalt Ltd","INV-004","Retainer May",3000,"Bank transfer"),
               (d(2026,7,3),"Acme Co","INV-005","Site update (part 1)",500,"Stripe"),
               (d(2026,9,12),"Birch Studio","INV-006","Copywriting",1500,"PayPal"),
               (d(2025,12,15),"Acme Co","INV-000","Prior-year job",999,"Bank transfer")]
        for i, row in enumerate(inc, 5):
            for j, v in enumerate(row, 1): I.cell(row=i, column=j, value=v)
        exp = [(d(2026,1,5),"Adobe","Software & Subscriptions","Creative Cloud",600,None),
               (d(2026,2,10),"Apple","Equipment & Hardware","Monitor",400,None),
               (d(2026,4,15),"Verizon","Internet & Phone","Phone",1000,0.5),
               (d(2026,6,2),"Bistro","Meals (50%)","Client lunch",200,0.5),
               (d(2026,9,30),"Google Ads","Marketing & Advertising","Campaign",300,None)]
        for i, row in enumerate(exp, 5):
            for j, v in enumerate(row, 1): E.cell(row=i, column=j, value=v)
        inv = [("INV-001","Acme Co",d(2026,1,5),30,2500),("INV-002","Acme Co",d(2026,2,1),30,1800),
               ("INV-003","Birch Studio",d(2026,3,20),30,1200),("INV-004","Cobalt Ltd",d(2026,5,1),15,3000),
               ("INV-005","Acme Co",d(2026,6,15),30,1500),("INV-006","Birch Studio",d(2026,8,28),14,1500),
               ("INV-007","Cobalt Ltd",d(2099,1,1),30,800)]
        for i, row in enumerate(inv, 5):
            for j, v in zip((1,2,3,4,6), row): V.cell(row=i, column=j, value=v)
        for i, n in enumerate(["Acme Co","Birch Studio","Cobalt Ltd"], 5): C.cell(row=i, column=1, value=n)
    wb.save(os.path.join(OUT, "Freelancer_Finance_Tracker" + ("_DEMO" if demo else "") + ".xlsx"))

# ---------------------------------------------------------------- WORKBOOK 2
def build_deductions(demo):
    wb = Workbook()
    S = wb.active; S.title = "Settings"
    title(S, "Settings", "Mileage rates are per IRS notices for 2026 - verify at irs.gov before filing.")
    S["A4"] = "Tax year"; S["B4"] = 2026
    S["A5"] = "Business mileage rate, Jan 1 - Jun 30 ($/mile)"; S["B5"] = 0.725
    S["A6"] = "Business mileage rate, from rate-change date ($/mile)"; S["B6"] = 0.76
    S["A7"] = "Rate-change date"; S["B7"] = dt.date(2026,7,1); S["B7"].number_format = DATE
    S["A8"] = "Home office: simplified method rate ($/sq ft)"; S["B8"] = 5
    S["A9"] = "Home office: sq ft used exclusively for business (max 300)"; S["B9"] = 120
    S["A10"] = "Total home sq ft (for actual-expense method)"; S["B10"] = 900
    S["A11"] = "Combined marginal tax rate (for savings estimate)"; S["B11"] = 0.25; S["B11"].number_format = "0%"
    for r in range(4, 12): S.cell(row=r, column=2).fill = ifill; S.cell(row=r, column=2).border = box
    S.column_dimensions["A"].width = 62; S.column_dimensions["B"].width = 14
    S["A13"] = "Note: the mileage rate was reported raised mid-2026 (72.5c to 76c from Jul 1). If your rates differ, just edit B5:B7."

    M = wb.create_sheet("Mileage")
    title(M, "Mileage log", "Date, purpose and miles. Rate and deduction fill automatically.")
    header(M, 4, ["Date","Purpose / client","From","To","Miles","Rate","Deduction","Year"], [14,30,18,18,10,10,14,8])
    for r in range(5, 5+N):
        M.cell(row=r, column=6, value=f'=IF(OR(A{r}="",E{r}=""),"",IF(A{r}>=Settings!$B$7,Settings!$B$6,Settings!$B$5))')
        M.cell(row=r, column=7, value=f'=IF(F{r}="","",E{r}*F{r})').number_format = MONEY
        M.cell(row=r, column=8, value=f'=IF(A{r}="","",YEAR(A{r}))')
        M.cell(row=r, column=1).number_format = DATE; M.cell(row=r, column=6).number_format = '$0.000'
    style_inputs(M, 5, 4+N, range(1, 6))

    X = wb.create_sheet("Deductions")
    title(X, "Deduction log", "Every business cost you might deduct. Receipt column = Y/N so you can find gaps.")
    header(X, 4, ["Date","Item","Category","Amount","Business use %","Deductible","Receipt saved?","Year"], [14,32,26,13,14,14,14,8])
    for r in range(5, 5+N):
        X.cell(row=r, column=6, value=f'=IF(OR(A{r}="",D{r}=""),"",D{r}*IF(E{r}="",1,E{r}))').number_format = MONEY
        X.cell(row=r, column=8, value=f'=IF(A{r}="","",YEAR(A{r}))')
        X.cell(row=r, column=1).number_format = DATE; X.cell(row=r, column=4).number_format = MONEY; X.cell(row=r, column=5).number_format = "0%"
    style_inputs(X, 5, 4+N, range(1, 8))
    dvc = DataValidation(type="list", formula1='"' + ",".join(c for c in CATS if "," not in c) + '"', allow_blank=True)
    dvr = DataValidation(type="list", formula1='"Y,N"', allow_blank=True)
    X.add_data_validation(dvc); X.add_data_validation(dvr); dvc.add(f"C5:C{4+N}"); dvr.add(f"G5:G{4+N}")

    HO = wb.create_sheet("Home Office")
    title(HO, "Home office comparison", "Compares the simplified method with an actual-expense estimate. Enter annual household costs.")
    HO["A4"] = "Annual household cost"; HO["B4"] = "Amount"
    for c in "AB": HO[f"{c}4"].font = hfont; HO[f"{c}4"].fill = hfill
    items = [("Rent or mortgage interest",0),("Utilities",0),("Internet (home portion)",0),("Renters/home insurance",0),("Repairs & maintenance",0)]
    for i, (k, v) in enumerate(items, 5):
        HO.cell(row=i, column=1, value=k); c = HO.cell(row=i, column=2, value=v); c.fill = ifill; c.number_format = MONEY
    HO["A10"] = "Total household costs"; HO["B10"] = "=SUM(B5:B9)"
    HO["A11"] = "Business-use share"; HO["B11"] = "=IF(Settings!B10=0,0,MIN(Settings!B9,Settings!B10)/Settings!B10)"; HO["B11"].number_format = "0.0%"
    HO["A12"] = "Actual-expense deduction (estimate)"; HO["B12"] = "=B10*B11"
    HO["A13"] = "Simplified-method deduction (max 300 sq ft)"; HO["B13"] = "=MIN(Settings!B9,300)*Settings!B8"
    HO["A14"] = "Better method"; HO["B14"] = '=IF(B12>B13,"Actual expense","Simplified")'
    HO["A15"] = "Deduction to use"; HO["B15"] = "=MAX(B12,B13)"
    for r in (10, 12, 13, 15): HO[f"B{r}"].number_format = MONEY
    HO.column_dimensions["A"].width = 46; HO.column_dimensions["B"].width = 18

    SM = wb.create_sheet("Summary", 0)
    title(SM, "Tax Deduction & Mileage Summary")
    SM["A2"] = '="Tax year "&Settings!B4'
    rows = [("Mileage deduction", f'=SUMIFS(Mileage!$G$5:$G${4+N},Mileage!$H$5:$H${4+N},Settings!B4)'),
            ("Business miles", f'=SUMIFS(Mileage!$E$5:$E${4+N},Mileage!$H$5:$H${4+N},Settings!B4)'),
            ("Other deductions", f'=SUMIFS(Deductions!$F$5:$F${4+N},Deductions!$H$5:$H${4+N},Settings!B4)'),
            ("Home office deduction", "='Home Office'!B15"),
            ("TOTAL deductions", "=B4+B6+B7"),
            ("Estimated tax saved", "=B8*Settings!B11"),
            ("Items missing receipts", f'=COUNTIFS(Deductions!$G$5:$G${4+N},"N")')]
    for i, (k, f) in enumerate(rows, 4):
        SM.cell(row=i, column=1, value=k).font = Font(bold=True); SM.cell(row=i, column=1).fill = lfill
        c = SM.cell(row=i, column=2, value=f); c.font = Font(bold=True, color=NAVY)
        c.number_format = "#,##0.0" if k == "Business miles" else ("0" if "missing" in k else MONEY)
    SM["A12"] = "By category"; SM["A12"].font = Font(bold=True, color=NAVY)
    for i, cat in enumerate(CATS, 13):
        SM.cell(row=i, column=1, value=cat)
        SM.cell(row=i, column=2, value=f'=SUMIFS(Deductions!$F$5:$F${4+N},Deductions!$C$5:$C${4+N},A{i},Deductions!$H$5:$H${4+N},Settings!$B$4)').number_format = MONEY
    SM.column_dimensions["A"].width = 32; SM.column_dimensions["B"].width = 18
    pc = PieChart(); pc.title = "Deductions by category"; pc.height = 9; pc.width = 13
    pc.add_data(Reference(SM, min_col=2, min_row=13, max_row=26)); pc.set_categories(Reference(SM, min_col=1, min_row=13, max_row=26))
    SM.add_chart(pc, "D3")
    if demo:
        d = dt.date
        for i, row in enumerate([(d(2026,3,3),"Acme kickoff","Home","Acme HQ",40),(d(2026,6,20),"Client visit","Home","Cobalt",100),
                                 (d(2026,8,5),"Conference","Home","Expo",200),(d(2025,11,1),"Old trip","Home","X",999)], 5):
            for j, v in enumerate(row, 1): M.cell(row=i, column=j, value=v)
        for i, row in enumerate([(d(2026,1,5),"Laptop stand","Equipment & Hardware",100,None,"Y"),
                                 (d(2026,2,9),"Phone plan","Internet & Phone",600,0.5,"N"),
                                 (d(2026,3,1),"Online course","Education & Training",250,None,"Y")], 5):
            for j, v in zip((1,2,3,4,5,7), row): X.cell(row=i, column=j, value=v)
        HO["B5"] = 12000; HO["B6"] = 1800
    wb.save(os.path.join(OUT, "Freelancer_Tax_Deduction_Mileage_Tracker" + ("_DEMO" if demo else "") + ".xlsx"))

# ---------------------------------------------------------------- WORKBOOK 3
def build_rate(demo):
    wb = Workbook()
    R = wb.active; R.title = "Rate Calculator"
    title(R, "Freelance Rate Calculator", "Work backwards from the income you want to the hourly and day rate you must charge.")
    inp = [("Desired annual take-home pay", 60000 if demo else 0, MONEY),
           ("Annual business expenses", 6000 if demo else 0, MONEY),
           ("Annual health insurance / retirement you fund", 5000 if demo else 0, MONEY),
           ("Estimated total tax rate (SE + income + state)", 0.30, "0%"),
           ("Weeks worked per year (after holidays, vacation)", 46, "0"),
           ("Hours per week you work", 40, "0"),
           ("Billable share of working hours", 0.60, "0%"),
           ("Profit buffer", 0.10, "0%")]
    for i, (k, v, nf) in enumerate(inp, 4):
        R.cell(row=i, column=1, value=k); c = R.cell(row=i, column=2, value=v); c.number_format = nf; c.fill = ifill; c.border = box
    out = [("Revenue needed before tax", "=(B4+B6)/(1-B7)+B5"),
           ("Revenue needed incl. profit buffer", "=B13*(1+B11)"),
           ("Billable hours per year", "=B8*B9*B10"),
           ("MINIMUM HOURLY RATE", "=IF(B15=0,0,B14/B15)"),
           ("Day rate (7 billable hrs)", "=B16*7"),
           ("Project rate for 20 hours", "=B16*20"),
           ("Monthly revenue target", "=B14/12")]
    R["A12"] = "Results"; R["A12"].font = Font(bold=True, color=NAVY)
    for i, (k, f) in enumerate(out, 13):
        R.cell(row=i, column=1, value=k).font = Font(bold=True); R.cell(row=i, column=1).fill = lfill
        c = R.cell(row=i, column=2, value=f); c.number_format = "#,##0" if "hours per year" in k else MONEY; c.font = Font(bold=True, color=NAVY)
    R.column_dimensions["A"].width = 52; R.column_dimensions["B"].width = 18
    R["A21"] = "Tip: billable share is usually 50-70% for freelancers - admin, sales and invoicing eat the rest."

    P = wb.create_sheet("Project Profitability")
    title(P, "Project profitability", "Quote vs reality. Find out which clients and project types actually pay you well.")
    header(P, 4, ["Project","Client","Quoted price","Est. hours","Actual hours","Direct costs","Profit","Effective hourly","Target hourly","vs target","Verdict"],
           [26,20,14,11,12,13,13,15,13,12,16])
    for r in range(5, 5+200):
        P.cell(row=r, column=7, value=f'=IF(C{r}="","",C{r}-IF(F{r}="",0,F{r}))').number_format = MONEY
        P.cell(row=r, column=8, value=f'=IF(OR(C{r}="",E{r}="",E{r}=0),"",G{r}/E{r})').number_format = MONEY
        P.cell(row=r, column=9, value=f"=IF(C{r}=\"\",\"\",'Rate Calculator'!$B$16)").number_format = MONEY
        P.cell(row=r, column=10, value=f'=IF(OR(H{r}="",I{r}=""),"",H{r}-I{r})').number_format = MONEY
        P.cell(row=r, column=11, value=f'=IF(H{r}="","",IF(H{r}>=I{r},"On target",IF(H{r}>=0.7*I{r},"Underpriced","Money loser")))')
        for c in (3, 6): P.cell(row=r, column=c).number_format = MONEY
    style_inputs(P, 5, 204, [1, 2, 3, 4, 5, 6])
    P.conditional_formatting.add("K5:K204", CellIsRule(operator="equal", formula=['"Money loser"'], fill=PatternFill("solid", bgColor="F8CBAD", fgColor="F8CBAD")))
    P.conditional_formatting.add("K5:K204", CellIsRule(operator="equal", formula=['"On target"'], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    P["M4"] = "Totals"; P["M4"].font = Font(bold=True)
    P["M5"] = "Revenue"; P["N5"] = "=SUM(C5:C204)"
    P["M6"] = "Profit"; P["N6"] = "=SUM(G5:G204)"
    P["M7"] = "Hours"; P["N7"] = "=SUM(E5:E204)"
    P["M8"] = "Blended hourly"; P["N8"] = '=IF(N7=0,0,SUMIFS(G5:G204,E5:E204,">0")/N7)'
    P["M9"] = "Hours over estimate"; P["N9"] = '=SUMPRODUCT((D5:D204<>"")*(E5:E204<>"")*(E5:E204-D5:D204))'
    for r in (5, 6, 8): P[f"N{r}"].number_format = MONEY
    P.column_dimensions["M"].width = 20; P.column_dimensions["N"].width = 14

    T = wb.create_sheet("Time Log")
    title(T, "Time log", "Log hours per project. Weekly total shows your real billable load.")
    header(T, 4, ["Date","Project","Hours","Billable? (Y/N)","Notes","Week starts"], [14,28,10,14,34,14])
    for r in range(5, 5+500):
        T.cell(row=r, column=6, value=f'=IF(A{r}="","",A{r}-WEEKDAY(A{r},2)+1)').number_format = DATE
        T.cell(row=r, column=1).number_format = DATE
    style_inputs(T, 5, 504, range(1, 6))
    T["H4"] = "Total hours"; T["I4"] = "=SUM(C5:C504)"
    T["H5"] = "Billable hours"; T["I5"] = '=SUMIFS(C5:C504,D5:D504,"Y")'
    T["H6"] = "Billable share"; T["I6"] = '=IF(I4=0,0,I5/I4)'; T["I6"].number_format = "0.0%"
    T.column_dimensions["H"].width = 16
    if demo:
        d = dt.date
        for i, row in enumerate([("Logo pack","Acme Co",1500,15,20,50),("Website","Birch Studio",4000,40,38,200),
                                 ("Newsletter","Cobalt Ltd",600,6,16,0)], 5):
            for j, v in enumerate(row, 1): P.cell(row=i, column=j, value=v)
        for i, row in enumerate([(d(2026,9,7),"Logo pack",5,"Y","sketches"),(d(2026,9,8),"Website",6,"Y",""),
                                 (d(2026,9,9),"Admin",2,"N","invoicing"),(d(2026,9,14),"Website",4,"Y","")], 5):
            for j, v in enumerate(row, 1): T.cell(row=i, column=j, value=v)
    wb.save(os.path.join(OUT, "Freelancer_Rate_and_Project_Profit_Calculator" + ("_DEMO" if demo else "") + ".xlsx"))

if __name__ == "__main__":
    for demo in (False, True):
        build_finance(demo); build_deductions(demo); build_rate(demo)
    print("done")
