import { Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import DomainSelection from './pages/DomainSelection.jsx'
import Interview from './pages/Interview.jsx'
import Results from './pages/Results.jsx'
import History from './pages/History.jsx'


export default function App() {
  return (
    <>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/domains" element={<DomainSelection />} />
          <Route path="/interview" element={<Interview />} />
          <Route path="/results" element={<Results />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </main>
    </>
  )
}