import { useEffect, useState } from 'react'
import api from '../services/api.js'
import Spinner from '../components/Spinner.jsx'
import ErrorBox from '../components/ErrorBox.jsx'
import FeedbackCard from '../components/FeedbackCard.jsx'

export default function History() {
  const [sessions, setSessions] = useState(null)
  const [detail, setDetail] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/sessions').then(r => setSessions(r.data)).catch(() => setError('Chargement impossible'))
  }, [])

  const open = async (id) => {
    try {
      const r = await api.get(`/sessions/${id}`)
      setDetail(r.data)
    } catch {
      setError('Détail introuvable')
    }
  }

  if (!sessions) return <Spinner text="Chargement de l'historique…" />

  return (
    <div>
      <h1>Historique des sessions</h1>
      <ErrorBox message={error} />
      {sessions.length === 0 && <p>Aucune session enregistrée pour le moment.</p>}
      <div className="cards-grid">
        {sessions.map(s => (
          <div key={s.id} className="card clickable" onClick={() => open(s.id)}>
            <h3>#{s.id} — {s.domain}</h3>
            <p>Niveau : {s.level}</p>
            <p>Score : {s.score != null ? `${Math.round(s.score)}/100` : 'non terminé'}</p>
            <p className="muted">{new Date(s.created_at).toLocaleString('fr-FR')}</p>
          </div>
        ))}
      </div>
      {detail && (
        <div className="mt">
          <h2>Détail de la session #{detail.session.id}</h2>
          {detail.questions.map(q => (
            <div key={q.id} className="mb">
              <h4 className="q-title">{q.content}</h4>
              {q.answer ? (
                <>
                  <p className="muted">Votre réponse : {q.answer.content.slice(0, 150)}…</p>
                  <FeedbackCard evaluation={q.answer} />
                </>
              ) : (
                <p className="muted">Sans réponse</p>
              )}
            </div>
          ))}
          <button className="btn" onClick={() => setDetail(null)}>Fermer</button>
        </div>
      )}
    </div>
  )
}