import { Bell, Globe } from "lucide-react";

export default function Navbar({ userName = "Rohit Kumar", role = "Patient" }) {
  return (
    <header className="h-14 bg-white border-b border-gray-100 flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
          <span className="text-white text-xs font-bold">M</span>
        </div>
        <span className="font-semibold text-gray-800 text-sm">Mama Care</span>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1 text-sm text-gray-500 cursor-pointer hover:text-gray-700">
          <Globe size={14} />
          <span>English</span>
        </div>
        <div className="relative cursor-pointer">
          <Bell size={18} className="text-gray-500 hover:text-gray-700" />
          <span className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center leading-none">
            2
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-sm font-semibold text-blue-600">
            {userName[0]}
          </div>
          <div className="text-xs">
            <p className="font-medium text-gray-800">{userName}</p>
            <p className="text-gray-400">{role}</p>
          </div>
        </div>
      </div>
    </header>
  );
}