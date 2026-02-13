'use client'
import { useEffect, useState } from 'react'
import SpectrumPlot from '../../../components/SpectrumPlot'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function MaterialDetail({ params }: { params: { id: string } }) {
  const [material, setMaterial] = useState<any>(null)
  const [spectra, setSpectra] = useState<any[]>([])

  useEffect(() => {
    fetch(`${API}/materials/${params.id}`).then((r) => r.json()).then(setMaterial)
    fetch(`${API}/spectra?material_id=${params.id}&min_nm=900&max_nm=2500`).then((r) => r.json()).then(setSpectra)
  }, [params.id])

  if (!material) return <p>Loading…</p>

  return (
    <div>
      <h2>{material.name}</h2>
      <p>Category: {material.category}</p>
      <h3>Cite this spectrum</h3>
      {spectra.map((s) => (
        <div key={s.id} style={{ border: '1px solid #ddd', margin: '8px 0', padding: 8 }}>
          <p>Spectrum #{s.id} | type={s.value_type}</p>
          <p>Source URL: {s.provenance?.original_url}</p>
          <p>Citation: Retrieved from source on current API load date.</p>
          <a href={`${API}/spectra/${s.id}/download?format=csv`} target="_blank">Download CSV</a>
        </div>
      ))}
      <SpectrumPlot spectra={spectra} />
    </div>
  )
}
