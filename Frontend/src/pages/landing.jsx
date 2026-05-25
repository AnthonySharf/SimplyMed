import { Link } from 'react-router-dom'
import SearchBar from '../components/search_bar.jsx'
import heroSvg from '../assets/hero.svg'

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#111111] flex flex-col">
      <nav className="flex items-center justify-between py-6" style={{ paddingLeft: '5%', paddingRight: '5%' }}>
        <span className="text-white font-semibold" style={{ fontSize: '34px' }}>SimplyMed</span>
        <div className="flex items-center gap-8">
          <Link to="/sign-in" className="text-white" style={{ fontSize: '21px' }}>Sign In</Link>
          <Link to="/sign-up" className="text-white" style={{ fontSize: '21px' }}>Sign Up</Link>
        </div>
      </nav>

      {/* Hero — designed for 1440px, fits one screen */}
      <div style={{
        height: 'calc(100vh - 64px)',
        width: '100%',
        overflow: 'hidden',
        display: 'grid',
        gridTemplateColumns: '1fr minmax(0, 1100px) 1fr',
        gridTemplateRows: '1fr',
        alignItems: 'center',
        paddingTop: '1%',
      }}>
        {/* SVG — full width, capped so it doesn't overflow viewport */}
        <img
          src={heroSvg}
          alt=""
          className="pointer-events-none select-none"
          style={{
            gridColumn: '1 / -1',
            gridRow: '1',
            width: '120%',
            maxHeight: 'calc(100vh - 64px)',
            objectFit: 'cover',
            objectPosition: 'top center',
            alignSelf: 'start',
            marginTop: '-5%',
            marginLeft: '2%',
            zIndex: 0,
          }}
        />

        {/* Center column */}
        <div
          className="flex flex-col items-center text-center"
          style={{ gridColumn: '2', gridRow: '1', zIndex: 1, padding: '0 32px', marginTop: '-8vh' }}
        >
          <h1
            className="text-white font-bold leading-tight mb-6"
            style={{ fontSize: '88px', letterSpacing: '-1.5px' }}
          >
            Understand your medication, simply.
          </h1>
          <SearchBar />
          <p className="text-[#A0A0A0] mt-4" style={{ fontSize: '19px' }}>
            Search any drug to see its side effects explained in plain English.
          </p>
        </div>
      </div>
    </div>
  )
}
