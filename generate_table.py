import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# === 1. Connect to Google Sheet ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("soltreasuries-bacb5dba61ae.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open("soltreasuries")
sheet = spreadsheet.worksheet("sol")
data = sheet.get_all_records()
df = pd.DataFrame(data)

# === 2. Format a single row ===
def format_value(val):
    return str(val) if val not in ["", None] else "-"

def render_row(row):
    return f"""
<tr>
  <td class="rank-column">{row['rank']}</td>
  <td class="name-column">{row['name']}</td>
  <td>{format_value(row['ticker'])}</td>
  <td>{format_value(row['Country'])}</td>
  <td>{format_value(row['market'])}</td>
  <td class="value-cell">{format_value(row['marketCap ($)'])}</td>
  <td class="value-cell">{format_value(row['enterpriseValue'])}</td>
  <td class="value-cell green-value">{format_value(row['mNAV'])}</td>
  <td class="value-cell">{format_value(row['sol_count'])}</td>
  <td class="value-cell">{format_value(row['sol_value'])}</td>
  <td class="value-cell">{format_value(row['Purchase price'])}</td>
  <td class="value-cell">{format_value(row['Total Invested (USD, M)'])}</td>
  <td class="value-cell green-value">{format_value(row['Raise program (USD, M)'])}</td>
  <td class="value-cell">{format_value(row['YtD Performance'])}</td>
</tr>
"""

# === 3. Group rows ===
table_html = {"all": "", "ser": "", "etf": ""}
for _, row in df.iterrows():
    html_row = render_row(row)
    category = str(row.get("type", "")).lower()
    table_html["all"] += html_row  # Always add to "all"
    if category == "ser":
        table_html["ser"] += html_row
    elif category == "etf":
        table_html["etf"] += html_row

# === 4. Inject into index.html ===
with open("index.html", "r") as f:
    html_content = f.read()

for section in ["all", "ser", "etf"]:
    start = html_content.find(f'<tbody id="{section}"')  # find tbody start
    start = html_content.find(">", start) + 1             # go past opening tag
    end = html_content.find("</tbody>", start)
    html_content = html_content[:start] + "\n" + table_html[section] + html_content[end:]

with open("index.html", "w") as f:
    f.write(html_content)