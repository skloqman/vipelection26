import os
import json
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')
DB_FILE = "/tmp/database.db"

BASE_ROSTER = [
  {"id":"FAC1","name":"Mr. Mujtaba Khan","grade":"Faculty & Staff","section":"Managing Director"},
  {"id":"FAC2","name":"Ms. Veena","grade":"Faculty & Staff","section":"Academic Director"},
  {"id":"FAC3","name":"Ms. Syeda Mahjabeen","grade":"Faculty & Staff","section":"Academic Coordinator"},
  {"id":"FAC4","name":"Ma. Asma Najeeb","grade":"Faculty & Staff","section":"Academic Incharge(FLK)"},
  {"id":"FAC5","name":"Mr. Wahed","grade":"Faculty & Staff","section":"Deeniyath HOD"},
  {"id":"FAC6","name":"Ms. Doris Shaik","grade":"Faculty & Staff","section":"Admin Incharge"},
  {"id":"FAC7","name":"Ms. Mahjabeen","grade":"Faculty & Staff","section":"Floor In Charge"},
  {"id":"FAC8","name":"Ms. Seema Jabbar","grade":"Faculty & Staff","section":"In Charge"},
  {"id":"FAC26","name":"Mr. Salman","grade":"Faculty & Staff","section":"Admin"},
  {"id":"FAC9","name":"Ms. Shazia","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC10","name":"Ms. Parveen","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC11","name":"Ms. Rubeena","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC12","name":"Ms. Yasmeen","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC13","name":"Ms. Heena","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC14","name":"Ms. Mariyam","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC15","name":"Ms. Asfiya","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC16","name":"Ms. Kahera","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC17","name":"Ms. Zoya","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC18","name":"Ms. Reshma","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC19","name":"Ms. Masarath","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC20","name":"Ms. Amena","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC21","name":"Ms. Maheen","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC22","name":"Mr. Jaleel","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC23","name":"Mr. Fuzail","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC24","name":"Mr. Loqman","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC25","name":"Mr. Mohiuddin","grade":"Faculty & Staff","section":"Teacher"},
  {"id":"FAC32","name":"Imran","grade":"Faculty & Staff","section":"Driver"},
  {"id":"FAC33","name":"Hameed","grade":"Faculty & Staff","section":"Driver"},
  {"id":"FAC27","name":"Khaled","grade":"Faculty & Staff","section":"Watch man"},
  {"id":"FAC28","name":"M. Jyoti","grade":"Faculty & Staff","section":"Supporting Staff"},
  {"id":"FAC29","name":"Savitri","grade":"Faculty & Staff","section":"Supporting Staff"},
  {"id":"FAC30","name":"Noor","grade":"Faculty & Staff","section":"Supporting Staff"},
  {"id":"FAC31","name":"Baleshwari","grade":"Faculty & Staff","section":"Supporting Staff"},
  {"id":"1","name":"Abdul Kabir","grade":"4","section":""},
  {"id":"2","name":"Ali Bin Sawood Bakoban","grade":"4","section":""},
  {"id":"3","name":"Ayesha Syed Hasan","grade":"4","section":""},
  {"id":"4","name":"Ayra Afsheen","grade":"4","section":""},
  {"id":"5","name":"BIBI AYESHA SIDDIQUA","grade":"4","section":""},
  {"id":"6","name":"Habeeb Khan","grade":"4","section":""},
  {"id":"7","name":"MAHER UNNISA","grade":"4","section":""},
  {"id":"8","name":"Maira Mujeeb Khan","grade":"4","section":""},
  {"id":"9","name":"Maryam Ismail Shareef","grade":"4","section":""},
  {"id":"10","name":"Mir Anas Ali","grade":"4","section":""},
  {"id":"11","name":"Mohammed Ibrahim","grade":"4","section":""},
  {"id":"12","name":"MOHAMMED MALIK KHAN","grade":"4","section":""},
  {"id":"13","name":"Mohammed Mizba Uddin","grade":"4","section":""},
  {"id":"14","name":"Mohammed Sohaan","grade":"4","section":""},
  {"id":"15","name":"Muhammad Ibrahim","grade":"4","section":""},
  {"id":"16","name":"Nida Fatima","grade":"4","section":""},
  {"id":"17","name":"Shaik Azaan","grade":"4","section":""},
  {"id":"18","name":"Syed Azaan Uddin","grade":"4","section":""},
  {"id":"19","name":"SYED FARHAN","grade":"4","section":""},
  {"id":"20","name":"Syed Mohammed Hussain","grade":"4","section":""},
  {"id":"21","name":"Syed Murtaza","grade":"4","section":""},
  {"id":"22","name":"Syed Mustafa","grade":"4","section":""},
  {"id":"23","name":"Syeda Hoorain","grade":"4","section":""},
  {"id":"24","name":"Syeda Zainab Afsheen","grade":"4","section":""},
  {"id":"25","name":"Tazkiya Tahreem","grade":"4","section":""},
  {"id":"26","name":"Zahra Fatima","grade":"4","section":""},
  {"id":"27","name":"ARHUM KHAN","grade":"5","section":""},
  {"id":"28","name":"BATUL FATIMA","grade":"5","section":""},
  {"id":"29","name":"DURAR HADI","grade":"5","section":""},
  {"id":"30","name":"KHADIJA FATIMA","grade":"5","section":""},
  {"id":"31","name":"MARIYAM FATIMA","grade":"5","section":""},
  {"id":"32","name":"MOHD AMMAR","grade":"5","section":""},
  {"id":"33","name":"ARZAN","grade":"5","section":""},
  {"id":"34","name":"MOHD FAIZ","grade":"5","section":""},
  {"id":"35","name":"MOHD MUHAMMED","grade":"5","section":""},
  {"id":"36","name":"ZAIN MAHMOOD","grade":"5","section":""},
  {"id":"37","name":"SYED AFFAN MEER","grade":"5","section":""},
  {"id":"38","name":"SYED AYAN AHMED","grade":"5","section":""},
  {"id":"39","name":"SYED MUHAMMMED","grade":"5","section":""},
  {"id":"40","name":"S. SAMAIRA NOOR","grade":"5","section":""},
  {"id":"41","name":"UMAIMA SHAIK","grade":"5","section":""},
  {"id":"42","name":"ZUNAIRA HYDER","grade":"5","section":""},
  {"id":"43","name":"ABDUL KABEER","grade":"6","section":""},
  {"id":"44","name":"ABDUL RAHMAN","grade":"6","section":""},
  {"id":"45","name":"AFEEFA FATIMA","grade":"6","section":""},
  {"id":"46","name":"AIZA SADIQ","grade":"6","section":""},
  {"id":"47","name":"ALEENA AZIN","grade":"6","section":""},
  {"id":"48","name":"ALIZA FATIMA","grade":"6","section":""},
  {"id":"49","name":"DANIYA LARAIB","grade":"6","section":""},
  {"id":"50","name":"JUVERIYA KAMAL","grade":"6","section":""},
  {"id":"51","name":"MADIHA BAKOOBAN","grade":"6","section":""},
  {"id":"52","name":"MOHD ABDUL RAYYAN","grade":"6","section":""},
  {"id":"53","name":"MOHAMMED SHUJA","grade":"6","section":""},
  {"id":"54","name":"SHAIK IBRAHIM","grade":"6","section":""},
  {"id":"55","name":"SYED AHMED ALI","grade":"6","section":""},
  {"id":"56","name":"SYED UZAIR","grade":"6","section":""},
  {"id":"57","name":"SYED ZUHAIR","grade":"6","section":""},
  {"id":"58","name":"TAMEEM RAHEEL BHAT","grade":"6","section":""},
  {"id":"59","name":"UMRA FATIMA","grade":"6","section":""},
  {"id":"60","name":"UZAIR KHAN","grade":"6","section":""},
  {"id":"61","name":"ZARA SALEEM","grade":"6","section":""},
  {"id":"62","name":"Abdullah Syed Hasan","grade":"7","section":""},
  {"id":"63","name":"Ahmed Bin Sawood Bakooban","grade":"7","section":""},
  {"id":"64","name":"Amatul Hameed Rumaisa","grade":"7","section":""},
  {"id":"65","name":"Ammara Faiz","grade":"7","section":""},
  {"id":"66","name":"Md Abdul Bari","grade":"7","section":""},
  {"id":"67","name":"Mohammed Abdul Salah","grade":"7","section":""},
  {"id":"68","name":"Mohammed Arhaan Uddin","grade":"7","section":""},
  {"id":"69","name":"Mohammed Rehan","grade":"7","section":""},
  {"id":"70","name":"Mohammed Shahriyar Khan","grade":"7","section":""},
  {"id":"71","name":"Mohd Arham Uddin","grade":"7","section":""},
  {"id":"72","name":"Shaik Abdul Fazl ur Rahman Quadri","grade":"7","section":""},
  {"id":"73","name":"Syed Khaja Ahsanuddin","grade":"7","section":""},
  {"id":"74","name":"Syed Rehan","grade":"7","section":""},
  {"id":"75","name":"Syed Yaheya Zain","grade":"7","section":""},
  {"id":"76","name":"Syeda Mahveen Fatima","grade":"7","section":""},
  {"id":"77","name":"Syeda Zunairah Begum","grade":"7","section":""},
  {"id":"78","name":"Uzair Imtiaz","grade":"7","section":""},
  {"id":"79","name":"Zunairah Amtul Aleem","grade":"7","section":""},
  {"id":"80","name":"Abdullah Syed Hasan","grade":"8","section":""},
  {"id":"81","name":"Ahmed Bin Sawood Bakooban","grade":"8","section":""},
  {"id":"82","name":"Amatul Hameed Rumaisa","grade":"8","section":""},
  {"id":"83","name":"Ammara Faiz","grade":"8","section":""},
  {"id":"84","name":"Md Abdul Bari","grade":"8","section":""},
  {"id":"85","name":"Mohammed Abdul Salah","grade":"8","section":""},
  {"id":"86","name":"Mohammed Arhaan Uddin","grade":"8","section":""},
  {"id":"87","name":"Mohammed Rehan","grade":"8","section":""},
  {"id":"88","name":"Mohammed Shahriyar Khan","grade":"8","section":""},
  {"id":"89","name":"Mohd Arham Uddin","grade":"8","section":""},
  {"id":"90","name":"Shaik Abdul Fazl ur Rahman Quadri","grade":"8","section":""},
  {"id":"91","name":"Syed Khaja Ahsanuddin","grade":"8","section":""},
  {"id":"92","name":"Syed Rehan","grade":"8","section":""},
  {"id":"93","name":"Syed Yaheya Zain","grade":"8","section":""},
  {"id":"94","name":"Syeda Mahveen Fatima","grade":"8","section":""},
  {"id":"95","name":"Syeda Zunairah Begum","grade":"8","section":""},
  {"id":"96","name":"Uzair Imtiaz","grade":"8","section":""},
  {"id":"97","name":"Zunairah Amtul Aleem","grade":"8","section":""}
]

def get_db_connection():
    """Safe on-demand connection factory that initializes files within active request cycles only."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS votes (position TEXT, candidate_id TEXT, ballot_type TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS voter_history (voter_id TEXT, ballot_type TEXT, count INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS server_config (config_key TEXT PRIMARY KEY, config_val TEXT)''')
    conn.commit()
    return conn

@app.route('/')
def home():
    # Trigger database check inside active route lifecycle to comply with Vercel's read-only builder context
    conn = get_db_connection()
    conn.close()
    return render_template('index.html')

@app.route('/api/get-initial-state')
def get_initial_state():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT config_val FROM server_config WHERE config_key='ballot_structure'")
    row = cursor.fetchone()
    structure = json.loads(row[0]) if row else None

    cursor.execute("SELECT config_val FROM server_config WHERE config_key='general_roster'")
    g_row = cursor.fetchone()
    general_roster = json.loads(g_row[0]) if g_row else BASE_ROSTER

    cursor.execute("SELECT config_val FROM server_config WHERE config_key='special_roster'")
    s_row = cursor.fetchone()
    special_roster = json.loads(s_row[0]) if s_row else [p for p in general_roster if p['grade'] == "Faculty & Staff"]

    cursor.execute("SELECT candidate_id, COUNT(*) FROM votes GROUP BY candidate_id")
    votes_tally = {r[0]: r[1] for r in cursor.fetchall()}
    
    cursor.execute("SELECT voter_id, count FROM voter_history WHERE ballot_type='general'")
    voters = {r[0]: r[1] for r in cursor.fetchall()}

    cursor.execute("SELECT voter_id, count FROM voter_history WHERE ballot_type='special'")
    special_voters = {r[0]: r[1] for r in cursor.fetchall()}
    conn.close()

    return jsonify({
        "structure": structure,
        "roster": general_roster,
        "specialRoster": special_roster,
        "votes": votes_tally,
        "voters": voters,
        "houseVoters": special_voters
    })

@app.route('/api/save-config', methods=['POST'])
def save_config():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO server_config (config_key, config_val) VALUES ('ballot_structure', ?)", (json.dumps(data),))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/save-rosters', methods=['POST'])
def save_rosters():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    if "general" in data:
        cursor.execute("INSERT OR REPLACE INTO server_config (config_key, config_val) VALUES ('general_roster', ?)", (json.dumps(data["general"]),))
    if "special" in data:
        cursor.execute("INSERT OR REPLACE INTO server_config (config_key, config_val) VALUES ('special_roster', ?)", (json.dumps(data["special"]),))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/cast-vote', methods=['POST'])
def cast_vote():
    data = request.json
    voter_id = data.get('voterId')
    ballot_type = data.get('ballotType')
    selections = data.get('selections')

    is_staff = str(voter_id).startswith("FAC")
    max_allowed = 2 if is_staff else 1

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT count FROM voter_history WHERE voter_id=? AND ballot_type=?", (voter_id, ballot_type))
    row = cursor.fetchone()
    voted_count = row[0] if row else 0

    if voted_count >= max_allowed:
        conn.close()
        return jsonify({"success": False, "error": "Voted limit reached."}), 400

    for pos, cand in selections.items():
        cursor.execute("INSERT INTO votes (position, candidate_id, ballot_type) VALUES (?, ?, ?)", (pos, cand, ballot_type))

    if voted_count == 0:
        cursor.execute("INSERT INTO voter_history (voter_id, ballot_type, count) VALUES (?, ?, 1)", (voter_id, ballot_type))
    else:
        cursor.execute("UPDATE voter_history SET count=? WHERE voter_id=? AND ballot_type=?", (voted_count + 1, voter_id, ballot_type))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "votes_remaining": max_allowed - (voted_count + 1)})

@app.route('/api/reset', methods=['POST'])
def reset_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS votes")
    cursor.execute("DROP TABLE IF EXISTS voter_history")
    conn.commit()
    conn.close()
    return jsonify({"success": True})
