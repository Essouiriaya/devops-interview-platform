export default function FeedbackCard({ evaluation }) {
  if (!evaluation) return null

  const color = evaluation.score >= 70 ? 'good' : evaluation.score >= 40 ? 'mid' : 'bad'

  return (
    <div className={`feedback-card ${color}`}>
      <div className="score-badge">{Math.round(evaluation.score)}/100</div>

      <p className="feedback-text">{evaluation.feedback}</p>

      {evaluation.strengths?.length > 0 && (
        <div className="feedback-section strengths">
          <h4>✅ Points forts</h4>
          <ul>
            {evaluation.strengths.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}

      {evaluation.improvements?.length > 0 && (
        <div className="feedback-section improvements">
          <h4>🔧 À améliorer</h4>
          <ul>
            {evaluation.improvements.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}
    </div>
  )
}