export default function DrugProfile({ profile }) {
  const fields = [
    { label: 'Purpose', key: 'purpose' },
    { label: 'Active Ingredients', key: 'active_ingredients' },
    { label: 'Warnings', key: 'warnings' },
    { label: 'Usage', key: 'usage' },
  ]

  return (
    <div className="space-y-5">
      {fields.map(({ label, key }) => (
        <div key={key}>
          <p className="text-[#A0A0A0] text-sm mb-1">{label}</p>
          <p className="text-white text-base" style={{ lineHeight: 1.7 }}>{profile[key]}</p>
        </div>
      ))}
    </div>
  )
}
