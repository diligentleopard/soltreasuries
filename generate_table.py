# generate_table.py
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# === 1. Connect to Google Sheet ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("soltreasuries-bacb5dba61ae.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open("soltreasuries")  # Replace with your actual sheet name
sheet = spreadsheet.worksheet("sol")        # Replace with your tab/sheet name
data = sheet.get_all_records()
df = pd.DataFrame(data)

# === 2. Convert to HTML table rows ===
def format_value(val):
    return str(val) if val not in ["", None] else "-"

html = ""
for _, row in df.iterrows():
    html += "<tr>\n"
    html += f'  <td class="rank-column">{row["rank"]}</td>\n'
    html += f'  <td class="name-column">{row["name"]}</td>\n'
    html += f'  <td>{format_value(row["ticker"])}</td>\n'
    html += f'  <td>{format_value(row["Country"])}</td>\n'
    html += f'  <td>{format_value(row["market"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["marketCap ($)"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["enterpriseValue"])}</td>\n'
    html += f'  <td class="value-cell green-value">{format_value(row["mNAV"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["sol_count"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["sol_value"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["Purchase price"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["Total Invested (USD, M)"])}</td>\n'
    html += f'  <td class="value-cell green-value">{format_value(row["Raise program (USD, M)"])}</td>\n'
    html += f'  <td class="value-cell">{format_value(row["YtD Performance"])}</td>\n'
    html += "</tr>\n"

# === 3. Inject into index.html ===
with open("index.html", "r") as f:
    html_content = f.read()

start = html_content.find('<tbody id="table-body">') + len('<tbody id="table-body">')
end = html_content.find('</tbody>', start)
new_html = html_content[:start] + "\n" + html + html_content[end:]

with open("index.html", "w") as f:
    f.write(new_html)