import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CalendarDays, ClipboardList, HeartPulse, LockKeyhole, Stethoscope, Users } from "lucide-react";
import { login, register } from "../services/api";

const roles = [
  { key: "patient", title: "Patient portal", text: "Reports, prescriptions and appointments", icon: HeartPulse },
  { key: "receptionist", title: "Reception desk", text: "Patient intake, documents and tokens", icon: Users },
  { key: "doctor", title: "Doctor workspace", text: "Queue, patient review and prescriptions", icon: Stethoscope },
];
const routes = { patient: "/patient/dashboard", receptionist: "/receptionist/dashboard", doctor: "/doctor/dashboard" };

export default function LandingPage() {
  const [role, setRole] = useState("patient"), [mode, setMode] = useState("login"), [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "" }), [message, setMessage] = useState("");
  const navigate = useNavigate();
  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const submit = async (e) => {
    e.preventDefault(); setMessage("");
    if (!/^\S+@\S+\.\S+$/.test(form.email)) return setMessage("Enter a valid email address.");
    if (form.password.length < 8) return setMessage("Password must be at least 8 characters.");
    setLoading(true);
    try {
      const response = mode === "login" ? await login({ email: form.email, password: form.password, role }) : await register({ ...form, role });
      const user = response.data.user;
      if (mode === "register") { setMode("login"); setMessage("Account created. Sign in with your new credentials."); }
      else { localStorage.setItem("mamacare_user", JSON.stringify(user)); navigate(routes[user.role]); }
    } catch (err) { setMessage(err.response?.data?.error || "Unable to reach the care server. Please try again."); }
    finally { setLoading(false); }
  };
  return <div className="min-h-screen bg-slate-50 flex">
    <aside className="hidden lg:flex w-72 bg-white border-r border-slate-200 flex-col p-6">
      <div className="flex items-center gap-2 font-semibold text-slate-800"><span className="p-2 rounded-lg bg-blue-600 text-white"><HeartPulse size={20}/></span><span>Mama Care</span></div>
      <p className="text-xs text-slate-400 mt-1 pl-10">Connected care platform</p>
      <div className="mt-10"><p className="text-[11px] font-semibold tracking-wider text-slate-400 px-3 mb-3">CARE ACCESS</p>{roles.map(({key,title,text,icon:Icon})=><button key={key} onClick={()=>{setRole(key);setMessage("")}} className={`w-full flex gap-3 items-start text-left p-3 rounded-xl mb-1 ${role===key?"bg-blue-50 text-blue-700":"text-slate-600 hover:bg-slate-50"}`}><Icon size={18} className="mt-0.5"/><span><b className="block text-sm">{title}</b><small className="text-xs text-slate-400">{text}</small></span></button>)}</div>
      <div className="mt-auto bg-slate-50 rounded-xl p-4"><LockKeyhole size={17} className="text-blue-600 mb-2"/><p className="font-medium text-sm">Your care, securely connected.</p><p className="text-xs leading-relaxed text-slate-500 mt-1">Only authorised patients and care staff can access relevant records.</p></div>
    </aside>
    <main className="flex-1 p-5 md:p-8 lg:p-10"><div className="max-w-5xl mx-auto"><div className="lg:hidden flex items-center gap-2 font-semibold text-slate-800 mb-8"><span className="p-2 rounded-lg bg-blue-600 text-white"><HeartPulse size={18}/></span>Mama Care</div><div className="mb-7"><p className="text-xs font-semibold text-blue-600 tracking-wider">{role.toUpperCase()} ACCESS</p><h1 className="text-2xl font-bold text-slate-800 mt-1">Welcome to your care workspace</h1><p className="text-sm text-slate-500 mt-1">Sign in to continue, or create a new account to get started.</p></div>
      <div className="grid lg:grid-cols-[1fr_.85fr] gap-6"><section className="bg-white rounded-2xl border border-slate-200 p-5 md:p-6"><p className="text-xs font-semibold text-slate-500 mb-2">CHOOSE YOUR PORTAL</p><div className="grid sm:grid-cols-3 gap-2 mb-5">{roles.map(({key,title,icon:Icon})=><button key={key} onClick={()=>{setRole(key);setMessage("")}} className={`text-left p-3 rounded-xl border text-xs ${role===key?"border-blue-600 bg-blue-50 text-blue-700":"border-slate-200 text-slate-600"}`}><Icon size={17} className="mb-1"/><b className="block">{title.replace(" portal", "").replace(" desk", "")}</b></button>)}</div><div className="flex border-b border-slate-200 mb-5"><button onClick={()=>{setMode("login");setMessage("")}} className={`pb-3 px-1 mr-6 text-sm font-medium border-b-2 ${mode==="login"?"border-blue-600 text-blue-600":"border-transparent text-slate-500"}`}>Sign in</button><button onClick={()=>{setMode("register");setMessage("")}} className={`pb-3 px-1 text-sm font-medium border-b-2 ${mode==="register"?"border-blue-600 text-blue-600":"border-transparent text-slate-500"}`}>Create account</button></div>
        <form onSubmit={submit} className="space-y-4">{mode==="register"&&<><div><label className="text-xs font-medium text-slate-600">Full name</label><input name="name" required value={form.name} onChange={change} className="input mt-1" placeholder="Enter your full name"/></div><div><label className="text-xs font-medium text-slate-600">Mobile number</label><input name="phone" value={form.phone} onChange={change} className="input mt-1" placeholder="Enter mobile number"/></div></>}<div><label className="text-xs font-medium text-slate-600">Email address</label><input name="email" type="email" required value={form.email} onChange={change} className="input mt-1" placeholder="name@example.com"/></div><div><label className="text-xs font-medium text-slate-600">Password</label><input name="password" type="password" minLength="8" required value={form.password} onChange={change} className="input mt-1" placeholder="Minimum 8 characters"/><p className="text-xs text-slate-400 mt-1">Use a valid email and at least 8 characters.</p></div>{message&&<p className="rounded-lg bg-amber-50 text-amber-800 px-3 py-2 text-sm">{message}</p>}<button disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg text-sm font-medium disabled:opacity-60">{loading?"Please wait...":mode==="login"?"Sign in to dashboard":"Create account"}</button></form></section>
      <section className="space-y-4"><div className="bg-white rounded-2xl border border-slate-200 p-5"><p className="text-sm font-semibold">After you sign in</p><div className="mt-4 space-y-4"><div className="flex gap-3"><span className="bg-blue-50 text-blue-600 p-2 rounded-lg h-fit"><ClipboardList size={18}/></span><div><b className="text-sm">One connected record</b><p className="text-xs text-slate-500 mt-1">Documents, insurance and clinical notes are available in the right workspace.</p></div></div><div className="flex gap-3"><span className="bg-violet-50 text-violet-600 p-2 rounded-lg h-fit"><CalendarDays size={18}/></span><div><b className="text-sm">Clear appointment flow</b><p className="text-xs text-slate-500 mt-1">Reception creates a token, doctors manage the queue, patients see updates.</p></div></div></div></div><div className="bg-blue-50 border border-blue-100 rounded-2xl p-5"><p className="font-semibold text-sm text-blue-900">Demo credentials</p><p className="text-xs text-blue-800 mt-2 leading-relaxed">Choose the matching role, then use:<br/>patient@mamacare.org<br/>doctor@mamacare.org<br/>reception@mamacare.org<br/><b>Password: password123</b></p></div></section></div></div></main>
  </div>;
}
