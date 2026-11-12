import { Link, NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="brand">
        <span className="brand-icon">🎯</span>
        <span className="brand-text">
          Interview <span className="brand-accent">Platform</span>
        </span>
      </Link>
      <div className="nav-links">
        <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>
          Dashboard
        </NavLink>
        <NavLink to="/domains" className={({ isActive }) => isActive ? 'active' : ''}>
          S'entraîner
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => isActive ? 'active' : ''}>
          Historique
        </NavLink>
      </div>
    </nav>
  )
}