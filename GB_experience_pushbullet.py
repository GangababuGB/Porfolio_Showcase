from datetime import datetime
import requests
import os
access_token = os.environ.get("PUSHBULLET_TOKEN")

# --- Experience calculation functions ---
def calculate_experience(start_date, end_date=None):
    start = datetime.strptime(start_date, "%d %b %Y")
    end = datetime.today() if end_date in [None, "Present"] else datetime.strptime(end_date, "%d %b %Y")
    
    delta_years = end.year - start.year
    delta_months = end.month - start.month
    delta_days = end.day - start.day
    
    if delta_days < 0:
        delta_months -= 1
        delta_days += (start.replace(month=start.month+1, day=1) - start.replace(day=1)).days
    if delta_months < 0:
        delta_years -= 1
        delta_months += 12
        
    return delta_years, delta_months, delta_days

def add_experience(exp_list):
    total_years = total_months = total_days = 0
    for exp in exp_list:
        y, m, d = calculate_experience(*exp)
        total_years += y
        total_months += m
        total_days += d
    
    total_months += total_days // 30
    total_days = total_days % 30
    total_years += total_months // 12
    total_months = total_months % 12
    
    return total_years, total_months, total_days

# --- Define periods ---
tata_comm = [("29 Jan 2018", "10 Sep 2021")]
great_learning = [("09 Oct 2019", "12 Oct 2021")]
roadmap_it = [("13 Sep 2021", "19 Jul 2022")]
nuvento = [("20 Jul 2022", "18 Jan 2023"),
           ("19 Jan 2023", "01 Apr 2024"),
           ("02 Apr 2024", "Present")]

# --- Calculate experiences ---
exp1 = add_experience(tata_comm)
exp2 = add_experience(great_learning + roadmap_it + nuvento)
exp3 = add_experience(roadmap_it + nuvento)
overall_exp = add_experience(tata_comm + roadmap_it + nuvento)

data = [
    ("❌ Exclude Non-IT (Tata Communication)", exp1),
    ("\n 🔄 Include Career Transition (Great Learning + Road Map IT + Nuvento)", exp2),
    ("\n 💼 Relevant Experience (Road Map IT + Nuvento)", exp3),
    ("\n 🌟 Overall Experience (Tata + IT roles, excluding Great Learning)", overall_exp)
]

# --- Pushbullet function ---
def send_pushbullet(title, body, access_token):
    headers = {
        "Access-Token": access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "type": "note",
        "title": title,
        "body": body
    }
    response = requests.post("https://api.pushbullet.com/v2/pushes", headers=headers, json=payload)
    return response.status_code, response.text

# --- Prepare Pushbullet message ---
message_body = ""
for desc, exp in data:
    message_body += f"{desc}: {exp[0]}y {exp[1]}m {exp[2]}d\n"

# Replace with your actual Pushbullet Access Token
status, text = send_pushbullet("Experience Summary", message_body, access_token)
print(f"Pushbullet Response: {status}, {text}")
