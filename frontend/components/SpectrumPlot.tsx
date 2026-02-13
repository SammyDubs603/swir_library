'use client'
import dynamic from 'next/dynamic'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export default function SpectrumPlot({ spectra }: { spectra: any[] }) {
  const data = spectra.map((s) => ({ x: s.wavelength_nm, y: s.value, type: 'scatter', mode: 'lines', name: `#${s.id} ${s.value_type}` }))
  return <Plot data={data} layout={{ title: 'Spectrum Overlay', xaxis: { title: 'Wavelength (nm)' }, yaxis: { title: 'Value' } }} />
}
