import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const [topic, setTopic] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [currentMessage, setCurrentMessage] = useState({ sender: '', content: '' })
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, currentMessage])

  const startDebate = async () => {
    if (!topic.trim()) {
      alert('Please enter a topic')
      return
    }

    setIsLoading(true)
    setMessages([])
    setCurrentMessage({ sender: '', content: '' })

    try {
      const response = await fetch('http://localhost:8000/debate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic: topic.trim() }),
      })

      if (!response.ok) {
        throw new Error('Failed to start debate')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              handleSSEMessage(data)
            } catch (e) {
              console.error('Failed to parse SSE message:', e)
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to start debate. Make sure the API server is running.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSSEMessage = (data) => {
    switch (data.type) {
      case 'topic':
        setMessages(prev => [...prev, { sender: data.sender, content: data.content }])
        break
      case 'start':
        setCurrentMessage({ sender: data.sender, content: '' })
        break
      case 'char':
        setCurrentMessage(prev => ({
          ...prev,
          content: prev.content + data.content
        }))
        break
      case 'complete':
        setMessages(prev => [...prev, { sender: data.sender, content: data.content }])
        setCurrentMessage({ sender: '', content: '' })
        break
      case 'error':
        setMessages(prev => [...prev, { sender: data.sender, content: `Error: ${data.message}` }])
        setCurrentMessage({ sender: '', content: '' })
        break
      case 'done':
        // Debate round completed
        break
      default:
        console.log('Unknown message type:', data.type)
    }
  }

  const resetDebate = async () => {
    try {
      await fetch('http://localhost:8000/debate/reset', {
        method: 'POST',
      })
      setMessages([])
      setCurrentMessage({ sender: '', content: '' })
      setTopic('')
    } catch (error) {
      console.error('Error resetting debate:', error)
    }
  }

  const nextRound = () => {
    if (topic.trim()) {
      startDebate()
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚔️ Battle of Models</h1>
        <p>AI Debate Simulation with Multiple Language Models</p>
      </header>

      <div className="container">
        <div className="chat-container">
          <div className="chat-history">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender.toLowerCase().replace(' ', '-')}`}>
                <div className="sender">{msg.sender}</div>
                <div className="content">{msg.content}</div>
              </div>
            ))}
            {currentMessage.sender && (
              <div className={`message ${currentMessage.sender.toLowerCase().replace(' ', '-')}`}>
                <div className="sender">{currentMessage.sender}</div>
                <div className="content typing">{currentMessage.content}<span className="cursor">|</span></div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <input
              type="text"
              className="topic-input"
              placeholder="Enter your debate topic..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !isLoading && startDebate()}
              disabled={isLoading}
            />
            <div className="button-group">
              <button 
                className="btn btn-primary" 
                onClick={startDebate} 
                disabled={isLoading || !topic.trim()}
              >
                {isLoading ? 'Debating...' : 'Start Debate'}
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={nextRound} 
                disabled={isLoading || !topic.trim()}
              >
                Next Round
              </button>
              <button 
                className="btn btn-danger" 
                onClick={resetDebate}
                disabled={isLoading}
              >
                Reset
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
