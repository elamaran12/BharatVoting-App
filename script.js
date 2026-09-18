let av=false,vv=false,user="",pick="";
const $=x=>document.getElementById(x);
function show(id){document.querySelectorAll(".page").forEach(x=>x.classList.remove("on"));$(id).classList.add("on");scrollTo(0,0)}
async function post(url,data){let r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});return r.json()}
async function sendOtp(){let d=await post("/api/aadhaar/send",{aadhaar:$("aadhaar").value});if(!d.ok)return $("amsg").textContent="Enter a valid 12-digit demo Aadhaar number."; $("otpbox").classList.remove("hide");$("otphint").textContent="Demo OTP: "+d.otp+" (real UIDAI OTP is not sent by this prototype)";$("amsg").textContent="OTP generated. Verify it below."}
async function verifyOtp(){let d=await post("/api/aadhaar/verify",{otp:$("otp").value});if(!d.ok)return $("amsg").textContent="Invalid OTP.";av=true;$("vbox").classList.remove("locked");$("amsg").textContent="✓ Aadhaar demo verification completed."}
async function verifyVoter(){if(!av)return $("vmsg").textContent="Complete Aadhaar verification first.";let d=await post("/api/voter/verify",{voter:$("voter").value});if(!d.ok)return $("vmsg").textContent="Enter a valid Voter ID.";vv=true;user=d.voter;$("vmsg").textContent="✓ Voter ID demo verification completed.";$("gohome").classList.remove("hide")}
async function login(){let d=await post("/api/login",{voter:$("loginid").value});if(!d.ok)return $("lmsg").textContent=d.msg||"Invalid User ID.";user=d.voter;show("voting")}
function party(p,b){pick=p;document.querySelectorAll(".parties button").forEach(x=>{x.classList.remove("selected");if(x!==b)x.classList.add("blocked")});b.classList.add("selected");$("sel").textContent="Selected: "+p;$("submit").classList.remove("disabled")}
async function vote(){let d=await post("/api/vote",{voter:user,party:pick});if(!d.ok)return alert(d.msg);$("tx").textContent="Transaction: "+d.tx;show("thanks")}
