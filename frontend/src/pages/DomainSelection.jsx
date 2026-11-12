import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api.js'
import Spinner from '../components/Spinner.jsx'
import ErrorBox from '../components/ErrorBox.jsx'

const LEVELS = ['débutant', 'intermédiaire', 'avancé']

export default function DomainSelection() {
  const [domains, setDomains] = useState([])
  const [selected, setSelected] = useState(null)
  const [level, setLevel] = useState('intermédiaire')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/domains')
      .then(r => setDomains(r.data.domains))
      .catch(() => setError('Impossible de charger les domaines'))
      .finally(() => setLoading(false))
  }, [])

  const start = () => {
    if (selected) navigate(`/interview?domain=${selected}&level=${level}`)
  }

  if (loading) return <Spinner text="Chargement des domaines…" />

  return (
    <div>
      <h1>Choisissez un domaine</h1>
      <ErrorBox message={error} />
      <div className="cards-grid">
        {domains.map(d => (
          <div key={d.id}
               className={`card clickable ${selected === d.id ? 'selected' : ''}`}
               onClick={() => setSelected(d.id)}>
            <h3>{d.name}</h3>
            <p>{d.description}</p>
          </div>
        ))}
      </div>
      <h2 className="mt">Niveau</h2>
      <div className="levels">
        {LEVELS.map(l => (
          <button key={l} className={`btn level ${level === l ? 'active' : ''}`} onClick={() => setLevel(l)}>
            {l}
          </button>
        ))}
      </div>
      <button className="btn primary big" disabled={!selected} onClick={start}>
        Générer les questions →
      </button>
    </div>
  )
}