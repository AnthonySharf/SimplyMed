export default function AdverseEvents({ events }) {
  return (
    <div>
      <ul className="space-y-4">
        {events.map(([name, { frequency }]) => (
          <li key={name} className="flex items-center gap-4">
            <span className="text-white text-sm w-52 shrink-0">{name}</span>
            <div className="flex-1 bg-[#2A2A2A] rounded-full h-1.5">
              <div className="bg-[#2DD4BF] h-1.5 rounded-full" style={{ width: `${frequency}%` }} />
            </div>
            <span className="text-[#A0A0A0] text-sm w-12 text-right shrink-0">{frequency}%</span>
          </li>
        ))}
      </ul>
      <p style={{ color: '#A0A0A0', fontSize: '0.75rem', fontStyle: 'italic', marginTop: '12px' }}>
        Frequencies are based on 500 FDA adverse event reports and represent how often each symptom was reported. They do not indicate the likelihood of experiencing these symptoms.
      </p>
    </div>
  )
}
