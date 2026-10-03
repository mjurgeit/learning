# Notion Freelancer OS - Build Guide (about 60-90 minutes)

You cannot generate a native Notion workspace from a file; Notion imports CSVs as databases and Markdown as pages.
Build once, publish a "Duplicate" link, and sell that link (see DELIVERY below).

## 1. Import the six databases
In Notion: sidebar > Import > CSV, one file at a time. Name each database exactly as the file (Clients, Projects, Tasks, Invoices, Money Log, Tax Periods).
Delete the "(sample)" rows later; keep them while you screenshot.

## 2. Set property types (Notion imports everything as text)
| Database | Property | Type |
|---|---|---|
| Clients | Status | Select: Lead, Active, Paused, Past |
| Clients | Source | Select: Referral, Upwork, LinkedIn, Social, Other |
| Clients | Rate Type | Select: Hourly, Project, Retainer |
| Clients | Hourly Rate | Number (dollar) |
| Projects | Client | Relation > Clients (two-way, "Projects") |
| Projects | Status | Select/Status: Proposal, In Progress, Review, Done, Lost |
| Projects | Quote, Direct Costs | Number (dollar) |
| Projects | Estimated Hours, Hours Logged | Number |
| Projects | Start Date, Due Date | Date |
| Tasks | Project | Relation > Projects |
| Tasks | Status | Status: To Do, In Progress, Done |
| Tasks | Priority | Select: High, Medium, Low |
| Tasks | Due | Date; Est. Minutes: Number |
| Invoices | Client | Relation > Clients; Project: Relation > Projects |
| Invoices | Issue Date | Date; Terms (days), Amount, Amount Paid: Number (dollar) |
| Money Log | Type | Select: Income, Expense |
| Money Log | Date | Date; Amount: Number (dollar); Deductible %: Number (percent, 100 = 100%) |
| Money Log | Category | Select (Software, Equipment, Home Office, Internet & Phone, Marketing, Education, Travel, Meals, Fees, Other, Client payment) |
| Money Log | Client | Relation > Clients |
| Tax Periods | Start, End, Due Date | Date |

## 3. Add formulas (Notion Formula 2.0 syntax; paste into a Formula property)
**Invoices**
- `Due Date`: `dateAdd(prop("Issue Date"), prop("Terms (days)"), "days")`
- `Balance`: `prop("Amount") - prop("Amount Paid")`
- `Status`: `if(prop("Balance") <= 0, "Paid", if(now() > prop("Due Date"), "Overdue", if(prop("Amount Paid") > 0, "Partial", "Open")))`
- `Days Overdue`: `if(prop("Status") == "Overdue", dateBetween(now(), prop("Due Date"), "days"), 0)`

**Projects**
- `Profit`: `prop("Quote") - prop("Direct Costs")`
- `Effective Hourly`: `if(prop("Hours Logged") > 0, round(prop("Profit") / prop("Hours Logged") * 100) / 100, 0)`
- `Hours Over Estimate`: `prop("Hours Logged") - prop("Estimated Hours")`
- `Invoiced` (Rollup): Invoices relation > Amount > Sum. Add a relation Projects <-> Invoices first (Invoices.Project already creates it).
- `Unbilled`: `prop("Quote") - prop("Invoiced")`

**Clients** (rollups via the Projects/Invoices relations)
- `Total Billed`: Rollup Invoices > Amount > Sum. `Outstanding`: Rollup Invoices > Balance > Sum.

**Money Log**
- `Deductible Amount`: `if(prop("Type") == "Expense", prop("Amount") * prop("Deductible %"), 0)` (if the percent property stores 50% as 0.5, this is right; if it stores 50, divide by 100)
- `Tax Period`: `if(month(prop("Date")) <= 3, "P1", if(month(prop("Date")) <= 5, "P2", if(month(prop("Date")) <= 8, "P3", "P4")))`
- `Year`: `year(prop("Date"))`

## 4. Dashboard page ("Freelancer OS - Home")
Create a page and add linked views (type /linked view of database):
1. Money Log - table, filter Type = Income and Year = 2026, group by Tax Period, show Sum of Amount in the footer.
2. Money Log - same with Type = Expense, footer Sum of Deductible Amount.
3. Invoices - board grouped by Status, filter Status is not Paid; sort Days Overdue descending.
4. Projects - board grouped by Status; show Effective Hourly and Hours Over Estimate.
5. Tasks - table filter Status is not Done, sort by Due; plus a "Today" view filtering Due = today.
6. Clients - gallery with Total Billed and Outstanding.
Optionally: Notion Charts view (Money Log, vertical bar, X = Month of Date, Y = Sum of Amount, group by Type).

## 5. Page templates
Add database templates: Projects ("New project": checklist Kickoff call, Contract signed, Deposit invoice sent, Draft, Revisions, Final invoice, Testimonial request), Clients ("New lead": discovery call questions), Invoices ("Standard invoice": net 14).
Reusable page text is in `Home_Page.md` and `Templates.md` (import via Import > Markdown & CSV).

## 6. Publish and package (DELIVERY)
1. Move everything under one parent page "Freelancer OS". Remove all "(sample)" data (or keep one demo copy: duplicate the page and call it "Freelancer OS - DEMO").
2. Share > Publish > enable "Allow duplicate as template". Copy the public link.
3. Delivery PDF (1-2 pages made in Canva or Google Docs): cover, the duplicate link (button), 5-step setup, support email.
4. Backup for buyers: zip of the six CSVs + this guide.
5. Notion Marketplace is optional: Notion charges 10% + $0.40 per transaction [verified, notion.com/help/selling-on-marketplace]; Etsy alone is fine to start.
6. Test: open the link in a private window logged into a different free Notion account, click Duplicate, confirm relations, formulas and views survived.
