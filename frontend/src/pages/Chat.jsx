import { useState } from 'react';
import apiClient from '../api/axiosConfig';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // We use a fixed session ID so the backend remembers the conversation context
  const SESSION_ID = 'react_frontend_1';

  const handleSendMessage = async (e) => {
    e.preventDefault(); // Prevents the page from refreshing on form submit
    if (!inputValue.trim()) return;

    // 1. Add user's message to the UI instantly
    const newMessages = [...messages, { role: 'user', content: inputValue }];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // 2. Send the request to Person C's FastAPI backend
      const response = await apiClient.post('/chat', {
        query: inputValue,
        session_id: SESSION_ID,
      });

      // 3. Add the AI's response to the UI
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.data.answer,
          sources: response.data.sources,
        },
      ]);
    } catch (error) {
      console.error("API Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '🚨 Error: Could not connect to the backend server.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h2>Agentic RAG Chat</h2>
      
      {/* Chat Window */}
      <div style={{ 
        height: '400px', overflowY: 'auto', border: '1px solid #ccc', 
        padding: '1rem', marginBottom: '1rem', borderRadius: '8px',
        display: 'flex', flexDirection: 'column', gap: '10px'
      }}>
        {messages.length === 0 && (
          <p style={{ color: '#888', textAlign: 'center' }}>Send a message to start!</p>
        )}
        
        {messages.map((msg, index) => (
          <div key={index} style={{
            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
            backgroundColor: msg.role === 'user' ? '#007bff' : '#f1f1f1',
            color: msg.role === 'user' ? 'white' : 'black',
            padding: '10px 14px',
            borderRadius: '16px',
            maxWidth: '80%'
          }}>
            <p style={{ margin: 0 }}>{msg.content}</p>
            {/* Display citations if the backend returned them */}
            {msg.sources && msg.sources.length > 0 && (
              <small style={{ display: 'block', marginTop: '8px', color: msg.role === 'user' ? '#cce5ff' : '#666' }}>
                 Source: {msg.sources.map(s => typeof s === 'string' ? s : JSON.stringify(s)).join(', ')}
               </small>
            )}
          </div>
        ))}
        
        {isLoading && <p style={{ color: '#888', fontStyle: 'italic' }}>AI is thinking...</p>}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question..."
          style={{ flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
          disabled={isLoading}
        />
        <button 
          type="submit" 
          disabled={isLoading}
          style={{ padding: '10px 20px', cursor: 'pointer', borderRadius: '4px', border: 'none', backgroundColor: '#28a745', color: 'white' }}
        >
          Send
        </button>
      </form>
    </div>
  );
}