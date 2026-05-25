import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function SearchBar({ className = '' }) {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  function handleKeyDown(e) {
    if (e.key === 'Enter' && query.trim()) {
      navigate(`/dashboard?drug=${encodeURIComponent(query.trim())}`)
    }
  }

  function handleClick() {
    if (query.trim()) {
      navigate(`/dashboard?drug=${encodeURIComponent(query.trim())}`)
    }
  }

  return (
    <div className={`w-full flex items-center bg-[#2E2E2E] border border-[#4A4A4A] focus-within:border-[#2DD4BF] rounded-full px-6 py-5 [box-shadow:1px_8px_30px_0_rgba(0,0,0,0.4)] ${className}`}>
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search a drug name..."
        className="flex-1 bg-transparent text-white placeholder-[#A0A0A0] outline-none" style={{ fontSize: '17.6px' }}
      />
      <button onClick={handleClick} className="ml-3 flex-shrink-0 cursor-pointer">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#A0A0A0" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </button>
    </div>
  )
}
