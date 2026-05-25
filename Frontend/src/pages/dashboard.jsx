import { useEffect, useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import DrugProfile from '../components/drug_profile.jsx'
import AdverseEvents from '../components/adverse_events.jsx'
import RedFlags from '../components/red_flags.jsx'
import SearchBar from '../components/search_bar.jsx'

export default function Dashboard() {
  const [searchParams] = useSearchParams()
  const drug = searchParams.get('drug')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!drug) return
    setLoading(true)
    setError(null)
    fetch(`http://localhost:8000/drug-info/${encodeURIComponent(drug)}`)
      .then(r => {
        if (!r.ok) throw new Error(`Error ${r.status}`)
        return r.json()
      })
      .then(d => { setData(d); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [drug])

  const regular = data
    ? Object.entries(data.adverse_events).filter(([name]) => !name.startsWith('⚠️'))
    : []
  const redFlags = data
    ? Object.entries(data.adverse_events).filter(([name]) => name.startsWith('⚠️'))
    : []

  function scrollTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  }

  const navLinks = [
    { label: 'Drug Profile', id: 'drug-profile' },
    { label: 'Adverse Events', id: 'adverse-events' },
    ...(redFlags.length > 0 ? [{ label: 'Red Flag Symptoms', id: 'red-flags' }] : []),
  ]

  const drugType = data?.drug_type

  return (
    <div className="min-h-screen bg-[#111111] text-white">

      {/* Sticky navbar */}
      <header className="sticky top-0 z-50 bg-[#1A1A1A] border-b border-[#2C2C2E] h-16 flex items-center px-12">
        <div className="w-40 shrink-0">
          <Link to="/" className="text-white font-semibold text-lg">SimplyMed</Link>
        </div>
        <div className="flex-1 flex justify-center">
          <SearchBar className="!max-w-xl !py-2.5 !px-5" />
        </div>
        <div className="w-40 shrink-0 flex justify-end items-center gap-6">
          <Link to="/sign-in" className="text-white text-sm">Sign In</Link>
          <Link to="/sign-up" className="text-white text-sm">Sign Up</Link>
        </div>
      </header>

      <div className="px-12 pt-10 pb-10" style={{ fontSize: '16px' }}>
        {loading && <p className="text-[#A0A0A0]">Loading...</p>}
        {error && <p className="text-red-400">{error}</p>}

        {data && (
          <>
            {/* Drug header */}
            <div className="flex items-center gap-3 mb-3" style={{ paddingTop: '40px' }}>
              <h1 className="font-bold capitalize" style={{ fontSize: '48px' }}>{data.drug_name}</h1>
              {drugType && (
                <span className="text-xs font-medium px-3 py-1 rounded-full border border-[#2C2C2E] text-[#A0A0A0] bg-[#1C1C1E] mt-1">
                  {drugType}
                </span>
              )}
            </div>
            <p className="text-[#A0A0A0] text-base mb-3" style={{ lineHeight: 1.7 }}>{data.drug_profile.purpose}</p>

            {/* Section nav */}
            <nav className="flex items-center mb-8 border-b border-[#2C2C2E] pb-4 mt-3">
              {navLinks.map((link, i) => (
                <span key={link.id} className="flex items-center">
                  {i > 0 && <span className="text-[#3A3A3A] mx-3">|</span>}
                  <button
                    onClick={() => scrollTo(link.id)}
                    className="text-[#2DD4BF] text-sm hover:opacity-80 cursor-pointer bg-transparent border-none p-0"
                  >
                    {link.label}
                  </button>
                </span>
              ))}
            </nav>

            {/* Two-column layout */}
            <div className="grid grid-cols-2 items-stretch" style={{ gap: '24px' }}>

              {/* Left — Drug Profile */}
              <section id="drug-profile" className="flex">
                <div className="bg-[#1C1C1E] border border-[#2C2C2E] rounded-xl flex-1" style={{ padding: '32px' }}>
                  <h2 className="text-lg font-semibold mb-5">Drug Profile</h2>
                  <DrugProfile profile={data.drug_profile} />
                </div>
              </section>

              {/* Right — Adverse Events + Red Flags */}
              <div className="flex flex-col" style={{ gap: '24px' }}>
                <section id="adverse-events">
                  <div className="bg-[#1C1C1E] border border-[#2C2C2E] rounded-xl" style={{ padding: '32px' }}>
                    <h2 className="text-lg font-semibold mb-5">Adverse Events</h2>
                    <AdverseEvents events={regular} />
                  </div>
                </section>

                {redFlags.length > 0 && (
                  <section id="red-flags">
                    <div className="bg-[#1C1C1E] border border-[#2C2C2E] rounded-xl" style={{ padding: '32px' }}>
                      <h2 className="text-lg font-semibold mb-5">Red Flag Symptoms</h2>
                      <RedFlags events={redFlags} />
                    </div>
                  </section>
                )}
              </div>
            </div>

            {/* Footnote */}
            <p className="text-[#A0A0A0] text-xs mt-8">
              Adverse event frequencies are estimated from FDA adverse event reports and may not reflect general population risk. Always consult a healthcare professional.
            </p>
          </>
        )}
      </div>
    </div>
  )
}
