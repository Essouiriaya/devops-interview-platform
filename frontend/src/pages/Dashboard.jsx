
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../services/api.js'
import ErrorBox from '../components/ErrorBox.jsx'

export default function Dashboard() {
  const [health, setHealth] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/health')
      .then(r => {
        setHealth(r.data)
        setError('')
      })
      .catch(() => setError('API injoignable'))
  }, [])

  const apiStatus = health
    ? 'online'
    : error
      ? 'offline'
      : 'checking'

  return (
    <main className="dashboard">

      {/* Hero section */}
      <section className="dashboard-hero">
        <div className="hero-content">
          <span className="hero-label">
            <span className="hero-label-dot" />
            AI-POWERED INTERVIEW PREPARATION
          </span>

          <h1>
            Your next opportunity
            <br />
            starts <span>with preparation.</span>
          </h1>

          <p className="hero-description">
            Practice technical interviews, test your knowledge
            and get intelligent feedback to improve your skills.
          </p>

          <div className="hero-actions">
            <Link to="/domains" className="primary-action">
              Start practicing <span>→</span>
            </Link>

            <Link to="/history" className="secondary-action">
              View my progress
            </Link>
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-glow" />
          <div className="visual-card">
            <div className="visual-card-top">
              <span className="visual-icon">✦</span>
              <span>AI INTERVIEW ASSISTANT</span>
            </div>

            <div className="visual-main-icon">AI</div>

            <h3>Ready to level up?</h3>
            <p>Your personal technical interview coach is ready.</p>

            <div className="visual-divider" />

            <div className="visual-bottom">
              <span>Practice</span>
              <span>Learn</span>
              <span>Improve</span>
            </div>
          </div>
        </div>
      </section>

      {/* API status */}
      <div className="dashboard-status">
        <div className="status-left">
          <span className={`status-indicator ${apiStatus}`} />
          <span>
            API status: <strong>
              {apiStatus === 'online'
                ? 'Connected'
                : apiStatus === 'checking'
                  ? 'Checking connection...'
                  : 'Offline'}
            </strong>
          </span>
        </div>

        {health && (
          <span className="database-label">
            {health.database === 'postgresql'
              ? 'PostgreSQL'
              : 'Demo mode'}
          </span>
        )}
      </div>

      <ErrorBox message={error} />

      {/* Main features */}
      <section className="dashboard-section">
        <div className="section-heading">
          <div>
            <span className="section-eyebrow">GET STARTED</span>
            <h2>What would you like to do?</h2>
          </div>
          <p>Choose your next step.</p>
        </div>

        <div className="dashboard-cards">

          <Link to="/domains" className="dashboard-feature-card practice-card">
            <div className="feature-top">
              <div className="feature-icon purple-icon">✦</div>
              <span className="feature-arrow">↗</span>
            </div>

            <div>
              <span className="feature-number">01 / PRACTICE</span>
              <h3>Start an interview</h3>
              <p>
                Choose your technical domain and difficulty level.
                Let AI generate questions and evaluate your answers.
              </p>
            </div>

            <span className="feature-link">
              Start a session <span>→</span>
            </span>
          </Link>

          <Link to="/history" className="dashboard-feature-card history-card">
            <div className="feature-top">
              <div className="feature-icon blue-icon">↗</div>
              <span className="feature-arrow">↗</span>
            </div>

            <div>
              <span className="feature-number">02 / PROGRESS</span>
              <h3>Track your progress</h3>
              <p>
                Review your previous interviews, explore your feedback
                and identify areas where you can improve.
              </p>
            </div>

            <span className="feature-link">
              View history <span>→</span>
            </span>
          </Link>

        </div>
      </section>

      {/* How it works */}
      <section className="dashboard-how">
        <span className="section-eyebrow">YOUR LEARNING JOURNEY</span>
        <h2>Practice smarter. Perform better.</h2>

        <div className="journey-steps">
          <div className="journey-step">
            <span>01</span>
            <div>
              <h4>Choose your domain</h4>
              <p>Select the technical subject you want to practice.</p>
            </div>
          </div>

          <div className="journey-step">
            <span>02</span>
            <div>
              <h4>Answer AI questions</h4>
              <p>Challenge yourself with generated interview questions.</p>
            </div>
          </div>

          <div className="journey-step">
            <span>03</span>
            <div>
              <h4>Get intelligent feedback</h4>
              <p>Understand your strengths and what to improve.</p>
            </div>
          </div>
        </div>
      </section>

    </main>
  )
}
