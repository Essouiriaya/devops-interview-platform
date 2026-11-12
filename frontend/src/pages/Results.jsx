import { Link, useLocation } from 'react-router-dom'
import FeedbackCard from '../components/FeedbackCard.jsx'

export default function Results() {
  const { state } = useLocation()
  if (!state?.results?.length) {
    return (
      <div>
        <h1>Résultats</h1>
        <p>Aucun résultat. Lancez d'abord un entraînement.</p>
        <Link className="btn primary" to="/domains">Commencer</Link>
      </div>
    )
  }
  const avg = state.results.reduce((s, r) => s + r.score, 0) / state.results.length
  return (
    <div>
      <h1>Résultats — {state.domain} <span className="level-tag">{state.level}</span></h1>
      <div className={`avg-score ${avg >= 70 ? 'good' : avg >= 40 ? 'mid' : 'bad'}`}>
        Score global : {Math.round(avg)} / 100
      </div>
      {state.results.map((r, i) => (
        <div key={i} className="mb">
          <h3 className="q-title">Q{i + 1}. {r.question}</h3>
          <FeedbackCard evaluation={r} />
        </div>
      ))}
      <div className="actions">
        <Link className="btn primary" to="/domains">Nouvel entraînement</Link>
        <Link className="btn" to="/history">Voir l'historique</Link>
      </div>
    </div>
  )
}