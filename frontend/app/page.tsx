'use client'
import { useEffect, useState } from 'react'
import SpectrumPlot from '../components/SpectrumPlot'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function HomePage() {
  const [materials, setMaterials] = useState<any[]>([])
  const [spectra, setSpectra] = useState<any[]>([])
  const [query, setQuery] = useState('')

  useEffect(() => {
    fetch(`${API}/materials`).then((r) => r.json()).then(setMaterials)
  }, [])

  const search = async () => {
    const mats = await fetch(`${API}/materials?query=${encodeURIComponent(query)}`).then((r) => r.json())
    setMaterials(mats)
    if (mats.length) {
      const specs = await fetch(`${API}/spectra?material_id=${mats[0].id}&min_nm=900&max_nm=2500`).then((r) => r.json())
      setSpectra(specs)
    } else {
      setSpectra([])
    }
  }

  return (
    <main>
      <div>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search material" />
        <button onClick={search}>Search</button>
      </div>
      <h3>Materials</h3>
      <ul>
        {materials.map((m) => <li key={m.id}><a href={`/materials/${m.id}`}>{m.name}</a> ({m.category})</li>)}
      </ul>
      {spectra.length > 0 && <SpectrumPlot spectra={spectra} />}
    </main>
  )
}
