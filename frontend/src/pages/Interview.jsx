import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import api from '../services/api.js'
import Spinner from '../components/Spinner.jsx'
import ErrorBox from '../components/ErrorBox.jsx'
import FeedbackCard from '../components/FeedbackCard.jsx'

export default function Interview() {
  const [params] = useSearchParams()
  const domain = params.get('domain')
  const level = params.get('level')
  const navigate = useNavigate()

  const [sessionId, setSessionId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [index, setIndex] = useState(0)
  const [answer, setAnswer] = useState('')
  const [evaluation, setEvaluation] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const start = async () => {
      try {
        setLoading(true)
        const s = await api.post('/sessions', { domain, level })
        setSessionId(s.data.id)
        const q = await api.post('/questions/generate', {
          domain, level, count: 5, session_id: s.data.id,
        })
        setQuestions(q.data)
      } catch {
        setError('Erreur lors de la génération des questions. Vérifiez que le backend est lancé.')
      } finally {
        setLoading(false)
      }
    }
    if (domain && level) start()
  }, [domain, level])

  const submit = async () => {
    if (!answer.trim()) return
    setLoading(true)
    setError('')
    try {
      const current = questions[index]
      const r = await api.post('/answers/evaluate', {
        question: current.question,
        answer,
        domain,
        level,
        session_id: sessionId,
        question_id: current.id ?? null,
      })
      setEvaluation(r.data)
      setResults(prev => [...prev, { question: current.question, ...r.data }])
    } catch {
      setError("Échec de l'évaluation. Réessayez.")
    } finally {
      setLoading(false)
    }
  }

  const next = () => {
    setAnswer('')
    setEvaluation(null)
    if (index + 1 >= questions.length) {
      navigate('/results', { state: { results, domain, level, sessionId } })
    } else {
      setIndex(index + 1)
    }
  }

  if (loading && questions.length === 0) return <Spinner text="Génération des questions par IA…" />

  if (questions.length === 0) {
    return <div><ErrorBox message={error || 'Aucune question générée.'} /></div>
  }

  const current = questions[index]

  return (
    <div>
      <h1>Entraînement — {domain} <span className="level-tag">{level}</span></h1>
      <p className="progress">Question {index + 1} / {questions.length}</p>
      <ErrorBox message={error} />

      <div className="question-card">
        <span className="difficulty">{current.difficulty}</span>
        <h2>{current.question}</h2>
        <textarea
          rows={8}
          placeholder="Rédigez votre réponse ici…"
          value={answer}
          onChange={e => setAnswer(e.target.value)}
          disabled={!!evaluation}
        />
        <div className="actions">
          {!evaluation ? (
            <button className="btn primary" onClick={submit} disabled={loading || !answer.trim()}>
              {loading ? 'Évaluation en cours…' : 'Soumettre ma réponse'}
            </button>
          ) : (
            <button className="btn primary" onClick={next}>
              {index + 1 >= questions.length ? 'Voir mes résultats →' : 'Question suivante →'}
            </button>
          )}
        </div>
      </div>

      {evaluation && <FeedbackCard evaluation={evaluation} />}
    </div>
  )
}