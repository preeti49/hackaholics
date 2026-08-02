import { NavLink } from "react-router-dom";
import { LayoutDashboard, Upload, FileText, History, Shield, Bell, Settings, LogOut } from "lucide-react";

const roleLinks = {
  patient: [
    { to: "/patient/dashboard", icon: <LayoutDashboard size={16}/>, label: "Dashboard" },
    { to: "/patient/dashboard", icon: <Upload size={16}/>, label: "Upload Report" },
    { to: "/patient/dashboard", icon: <FileText size={16}/>, label: "My Reports" },
    { to: "/patient/history", icon: <History size={16}/>, label: "Medical History" },
    { to: "/patient/dashboard", icon: <Shield size={16}/>, label: "Insurance Status" },
    { to: "/patient/dashboard", icon: <Bell size={16}/>, label: "Notifications" },
  ],
  receptionist: [
    { to: "/receptionist/dashboard", icon: <LayoutDashboard size={16}/>, label: "Dashboard" },
    { to: "/receptionist/workflow", icon: <Upload size={16}/>, label: "Upload Documents" },
    { to: "/receptionist/dashboard", icon: <FileText size={16}/>, label: "Extracted Information" },
    { to: "/receptionist/dashboard", icon: <Shield size={16}/>, label: "Insurance" },
    { to: "/receptionist/dashboard", icon: <Bell size={16}/>, label: "Missing Information" },
    { to: "/receptionist/dashboard", icon: <Bell size={16}/>, label: "Notifications" },
    { to: "/analytics", icon: <FileText size={16}/>, label: "Analytics" },
  ],
  doctor: [
    { to: "/doctor/dashboard", icon: <LayoutDashboard size={16}/>, label: "Dashboard" },
    { to: "/doctor/dashboard", icon: <FileText size={16}/>, label: "Today's Tokens" },
    { to: "/doctor/dashboard", icon: <History size={16}/>, label: "Patients" },
    { to: "/doctor/prescription", icon: <FileText size={16}/>, label: "Prescriptions" },
    { to: "/analytics", icon: <FileText size={16}/>, label: "Reports & Uploads" },
    { to: "/analytics", icon: <LayoutDashboard size={16}/>, label: "Analytics" },
  ],
};

export default function Sidebar({ role = "patient" }) {
  const links = roleLinks[role] || roleLinks.patient;
  return (
    <aside className="w-52 min-h-screen bg-white border-r border-gray-100 flex flex-col py-6 px-3">
      <div className="flex items-center gap-2 px-3 mb-8">
        <div className="w-7 h-7 bg-red-500 rounded-full flex items-center justify-center">
          <span className="text-white text-xs font-bold">M</span>
        </div>
        <span className="font-semibold text-gray-800 text-sm">Mama Care</span>
      </div>
      <nav className="flex flex-col gap-1 flex-1">
        {links.map((link) => (
          <NavLink
            key={link.label}
            to={link.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                isActive
                  ? "bg-blue-50 text-blue-600 font-medium"
                  : "text-gray-600 hover:bg-gray-50"
              }`
            }
          >
            {link.icon}
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="flex flex-col gap-1">
        <NavLink to="/" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-500 hover:bg-gray-50">
          <LogOut size={16}/> Logout
        </NavLink>
      </div>
    </aside>
  );
}