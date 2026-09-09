import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Chat from './pages/Chat';
import Dashboard from './pages/Dashboard';
import './App.css'; 

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #333', marginBottom: '2rem' }}>
        <Link to="/" style={{ marginRight: '20px', fontWeight: 'bold' }}>Chat Interface</Link>
        <Link to="/metrics" style={{ fontWeight: 'bold' }}>Observability Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/metrics" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;