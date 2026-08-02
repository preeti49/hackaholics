export default function UploadBox({ file, onChange, loading, onSubmit, label = "Upload File" }) {
  return (
    <div className="flex flex-col gap-3">
      <label className="border-2 border-dashed border-gray-200 rounded-xl p-8 flex flex-col items-center gap-2 cursor-pointer hover:border-blue-400 transition-colors">
        <span className="text-4xl">📄</span>
        <span className="text-sm text-gray-500 text-center">
          Drag & Drop your file here or click to browse
        </span>
        <span className="text-xs text-gray-400">Supports: PDF, JPG, PNG</span>
        {file && (
          <span className="text-xs text-blue-600 font-medium bg-blue-50 px-3 py-1 rounded-full">
            {file.name}
          </span>
        )}
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          className="hidden"
          onChange={(e) => onChange(e.target.files[0])}
        />
      </label>
      {onSubmit && (
        <button
          onClick={onSubmit}
          disabled={loading || !file}
          className="w-full bg-blue-600 text-white py-2.5 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Processing...
            </span>
          ) : label}
        </button>
      )}
    </div>
  );
}