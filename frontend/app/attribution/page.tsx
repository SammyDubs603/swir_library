'use client'
import { useEffect, useState } from 'react'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function AttributionPage() {
  const [sources, setSources] = useState<any[]>([])

  useEffect(() => {
    fetch(`${API}/sources`).then((r) => r.json()).then(setSources)
  }, [])

  return (
    <main>
      <h2>Attribution</h2>
      <ul>
        {sources.map((s) => (
          <li key={s.id}>
            <strong>{s.name}</strong> — {s.license}<br />
            {s.citation_text}<br />
            <a href={s.url} target="_blank">{s.url}</a>
          </li>
        ))}
      </ul>
    </main>
  )
}
