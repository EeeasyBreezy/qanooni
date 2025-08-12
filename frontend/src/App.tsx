import React from 'react'

export const App: React.FC = () => {
  const [name, setName] = React.useState<string>('World')
  const [message, setMessage] = React.useState<string>('')
  const [loading, setLoading] = React.useState<boolean>(false)
  const [error, setError] = React.useState<string | null>(null)

  const fetchGreeting = async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams({ name })
      const response = await fetch(`/api/greeting?${params.toString()}`)
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }
      const data: { message: string } = await response.json()
      setMessage(data.message)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  React.useEffect(() => {
    fetchGreeting().catch(() => undefined)
  }, [])

  return (
    <div style={{
      fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif',
      padding: '2rem',
      maxWidth: 680,
      margin: '0 auto'
    }}>
      <h1>FastAPI + React (Vite + TS)</h1>
      <p>Enter your name and get a greeting from the FastAPI backend.</p>
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Your name"
          style={{ padding: '0.5rem 0.75rem', fontSize: 16 }}
        />
        <button onClick={fetchGreeting} disabled={loading} style={{ padding: '0.5rem 0.75rem', fontSize: 16 }}>
          {loading ? 'Loading…' : 'Fetch greeting'}
        </button>
      </div>
      <div style={{ marginTop: 16 }}>
        {error && <p style={{ color: 'crimson' }}>Error: {error}</p>}
        {!error && message && <p><strong>Response:</strong> {message}</p>}
      </div>
      <hr style={{ margin: '2rem 0' }} />
      <p>Health check: <code>GET /api/health</code></p>
    </div>
  )
}


