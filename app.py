import sqlite3,uuid,random,json,os
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
B=Path(__file__).parent; DB=B/"bharat_voting.db"
def init():
 c=sqlite3.connect(DB);c.execute("CREATE TABLE IF NOT EXISTS votes(voter TEXT PRIMARY KEY,party TEXT,tx TEXT)");c.commit();c.close()
class H(BaseHTTPRequestHandler):
 def j(self,x,code=200):
  b=json.dumps(x).encode();self.send_response(code);self.send_header("Content-Type","application/json");self.send_header("Access-Control-Allow-Origin","*");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
 def do_OPTIONS(self):
  self.send_response(204);self.send_header("Access-Control-Allow-Origin","*");self.send_header("Access-Control-Allow-Methods","GET,POST");self.send_header("Access-Control-Allow-Headers","Content-Type");self.end_headers()
 def do_GET(self):
  p=self.path
  if p=="/": f="index.html";typ="text/html"
  elif p=="/style.css": f="style.css";typ="text/css"
  elif p=="/script.js": f="script.js";typ="application/javascript"
  else:
   if p=="/api/stats":
    c=sqlite3.connect(DB);n=c.execute("select count(*) from votes").fetchone()[0];c.close();return self.j({"votes":n})
   return self.send_error(404)
  b=(B/f).read_bytes();self.send_response(200);self.send_header("Content-Type",typ);self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
 def do_POST(self):
  n=int(self.headers.get("Content-Length",0));d=json.loads(self.rfile.read(n) or "{}");p=self.path
  if p=="/api/aadhaar/send":
   a=d.get("aadhaar","").replace(" ","")
   if len(a)!=12 or not a.isdigit(): return self.j({"ok":False,"msg":"Enter a 12-digit demo Aadhaar number."},400)
   otp=str(random.randint(100000,999999));return self.j({"ok":True,"otp":otp})
  if p=="/api/aadhaar/verify": return self.j({"ok":len(str(d.get("otp","")))==6})
  if p=="/api/voter/verify":
   v=d.get("voter","").strip().upper();return self.j({"ok":len(v)>=6,"voter":v})
  if p=="/api/login":
   v=d.get("voter","").strip().upper();c=sqlite3.connect(DB);used=c.execute("select 1 from votes where voter=?",(v,)).fetchone();c.close()
   if used:return self.j({"ok":False,"msg":"This demo voter has already voted."},409)
   return self.j({"ok":len(v)>=6,"voter":v})
  if p=="/api/vote":
   v=d.get("voter","").strip().upper();party=d.get("party")
   if party not in ("TVK","DMK","ADMK") or len(v)<6:return self.j({"ok":False,"msg":"Invalid voting request."},400)
   c=sqlite3.connect(DB)
   if c.execute("select 1 from votes where voter=?",(v,)).fetchone():c.close();return self.j({"ok":False,"msg":"Only one vote is allowed."},409)
   tx="BV-"+uuid.uuid4().hex[:16].upper();c.execute("insert into votes values(?,?,?)",(v,party,tx));c.commit();c.close();return self.j({"ok":True,"tx":tx})
  self.j({"ok":False},404)
init()
port = int(os.environ.get("PORT", 10000))
print(f"Bharat Voting App running on 0.0.0.0:{port}")
HTTPServer(("0.0.0.0", port), H).serve_forever()
