import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../services/api.js'
import ErrorBox from '../components/ErrorBox.jsx'

export default function Dashboard() {
  const [health, setHealth] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/health').then(r => setHealth(r.data)).catch(() => setError('API injoignable'))
  }, [])

  return (
    <div>
      <h1>Bienvenue 👋</h1>
      <p className="subtitle">
        Plateforme intelligente de préparation aux entretiens techniques.
        Génération de questions par IA (RAG + LLM) et évaluation automatique de vos réponses.
      </p>
      <div className="status-line">
        Statut API :{' '}
        {health ? (
          <span className="ok">● en ligne ({health.database === 'postgresql' ? 'PostgreSQL' : 'mode démo'})</span>
        ) : (
          <span className="ko">● hors ligne</span>
        )}
      </div>
      <ErrorBox message={error} />
      <div className="cards-grid">
        <Link to="/domains" className="card">
          <h3>🚀 Commencer un entraînement</h3>
          <p>Choisissez un domaine et un niveau, générez des questions sur mesure.</p>
        </Link>
        <Link to="/history" className="card">
          <h3>📊 Mon historique</h3>
          <p>Retrouvez vos sessions passées et suivez votre progression.</p>
        </Link>
      </div>
    </div>
  )
}