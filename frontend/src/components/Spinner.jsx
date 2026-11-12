export default function Spinner({ text = 'Chargement…' }) {
  return <div className="spinner-box"><div className="spinner" />{text}</div>
}