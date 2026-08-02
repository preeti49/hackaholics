import { useState } from "react";
import { Bot, Send, X } from "lucide-react";

export default function AiAssistant({ context = "care" }) {
  const [open, setOpen] = useState(false), [text, setText] = useState(""), [messages, setMessages] = useState([]);
  const ask = () => {
    if (!text.trim()) return;
    setMessages([...messages, { mine: true, text }, { text: context === "prescription" ? "I can help you draft clear prescription advice and medicine instructions. Please verify every clinical decision before saving." : "I can help explain appointments, reports and care information in your preferred language. For urgent symptoms, contact emergency services." }]);
    setText("");
  };
  return <div className="fixed bottom-5 right-5 z-50">
    {open && <div className="mb-3 w-80 bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden"><div className="bg-blue-600 text-white px-4 py-3 flex justify-between items-center"><span className="font-semibold text-sm flex gap-2 items-center"><Bot size={18}/> Mama Care AI</span><button onClick={()=>setOpen(false)}><X size={18}/></button></div><div className="p-3 h-52 overflow-auto space-y-2 text-sm"><p className="text-slate-600 bg-slate-50 p-2 rounded-lg">How can I help with your {context === "prescription" ? "prescription" : "care"} today?</p>{messages.map((m,i)=><p key={i} className={`p-2 rounded-lg ${m.mine?"bg-blue-50 text-blue-800 ml-6":"bg-slate-50 text-slate-600 mr-3"}`}>{m.text}</p>)}</div><div className="p-3 border-t flex gap-2"><input value={text} onChange={e=>setText(e.target.value)} onKeyDown={e=>e.key==="Enter"&&ask()} className="input py-2" placeholder="Ask in any language"/><button onClick={ask} className="bg-blue-600 text-white px-3 rounded-lg"><Send size={16}/></button></div></div>}
    <button onClick={()=>setOpen(!open)} className="bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg w-14 h-14 flex items-center justify-center" aria-label="Open AI assistant"><Bot size={25}/></button>
  </div>;
}
