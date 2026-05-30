import { useState } from "react"
import axios from "axios"

const API = "http://127.0.0.1:8000"

export default function App() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [pdfReady, setPdfReady] = useState(false)
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [filename, setFilename] = useState("")

  async function handleUpload() {
    if (!file) return
    setUploading(true)
    const formData = new FormData()
    formData.append("file", file)
    try {
      const res = await axios.post(`${API}/upload`, formData)
      setFilename(res.data.filename)
      setPdfReady(true)
      setMessages([{
        role: "assistant",
        content: `✅ "${res.data.filename}" loaded! ${res.data.chunks} chunks indexed. Ask me anything about it.`
      }])
    } catch (err) {
      alert("Upload failed: " + err.response?.data?.detail)
    }
    setUploading(false)
  }

  async function handleAsk() {
    if (!question.trim() || !pdfReady) return
    const userMsg = { role: "user", content: question }
    setMessages(prev => [...prev, userMsg])
    setQuestion("")
    setLoading(true)
    try {
      const res = await axios.post(`${API}/chat`, { question })
      const botMsg = {
        role: "assistant",
        content: res.data.answer,
        sources: res.data.sources
      }
      setMessages(prev => [...prev, botMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Error: " + err.response?.data?.detail
      }])
    }
    setLoading(false)
  }

  return (
    <div style={styles.app}>
      <div style={styles.container}>

        {/* Header */}
        <div style={styles.header}>
          <h1 style={styles.title}>📄 PDF Chat</h1>
          <p style={styles.subtitle}>Upload a PDF and ask questions about it</p>
        </div>

        {/* Upload Section */}
        <div style={styles.uploadBox}>
          <input
            type="file"
            accept=".pdf"
            onChange={e => setFile(e.target.files[0])}
            style={styles.fileInput}
          />
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            style={styles.uploadBtn}
          >
            {uploading ? "Processing..." : "Upload PDF"}
          </button>
          {pdfReady && <span style={styles.badge}>✅ {filename}</span>}
        </div>

        {/* Chat Window */}
        <div style={styles.chatWindow}>
          {messages.length === 0 && (
            <div style={styles.empty}>Upload a PDF to start chatting</div>
          )}
          {messages.map((msg, i) => (
            <div key={i} style={msg.role === "user" ? styles.userMsg : styles.botMsg}>
              <div style={styles.msgContent}>{msg.content}</div>
              {msg.sources && (
                <div style={styles.sources}>
                  <p style={styles.sourcesTitle}>📎 Sources:</p>
                  {msg.sources.map((s, j) => (
                    <div key={j} style={styles.sourceChunk}>{s}</div>
                  ))}
                </div>
              )}
            </div>
          ))}
          {loading && <div style={styles.botMsg}>⏳ Thinking...</div>}
        </div>

        {/* Input */}
        <div style={styles.inputRow}>
          <input
            style={styles.input}
            placeholder={pdfReady ? "Ask a question..." : "Upload a PDF first"}
            value={question}
            disabled={!pdfReady}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleAsk()}
          />
          <button
            onClick={handleAsk}
            disabled={!pdfReady || loading}
            style={styles.sendBtn}
          >
            Send
          </button>
        </div>

      </div>
    </div>
  )
}

const styles = {
  app: { minHeight: "100vh", background: "#0f0f0f", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "sans-serif" },
  container: { width: "100%", maxWidth: "780px", padding: "24px", display: "flex", flexDirection: "column", gap: "16px" },
  header: { textAlign: "center" },
  title: { color: "#ffffff", fontSize: "28px", margin: 0 },
  subtitle: { color: "#888", fontSize: "14px", marginTop: "6px" },
  uploadBox: { display: "flex", alignItems: "center", gap: "12px", background: "#1a1a1a", padding: "16px", borderRadius: "12px", flexWrap: "wrap" },
  fileInput: { color: "#ccc", flex: 1 },
  uploadBtn: { background: "#6c63ff", color: "#fff", border: "none", padding: "10px 20px", borderRadius: "8px", cursor: "pointer", fontWeight: "bold" },
  badge: { color: "#4caf50", fontWeight: "bold", fontSize: "13px" },
  chatWindow: { background: "#1a1a1a", borderRadius: "12px", padding: "20px", minHeight: "360px", maxHeight: "460px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "12px" },
  empty: { color: "#555", textAlign: "center", marginTop: "120px" },
  userMsg: { alignSelf: "flex-end", background: "#6c63ff", color: "#fff", padding: "12px 16px", borderRadius: "12px 12px 0 12px", maxWidth: "75%" },
  botMsg: { alignSelf: "flex-start", background: "#2a2a2a", color: "#eee", padding: "12px 16px", borderRadius: "12px 12px 12px 0", maxWidth: "85%" },
  msgContent: { lineHeight: "1.5" },
  sources: { marginTop: "10px", borderTop: "1px solid #444", paddingTop: "8px" },
  sourcesTitle: { color: "#888", fontSize: "12px", margin: "0 0 6px 0" },
  sourceChunk: { background: "#1a1a1a", color: "#aaa", fontSize: "12px", padding: "6px 10px", borderRadius: "6px", marginBottom: "4px", lineHeight: "1.4" },
  inputRow: { display: "flex", gap: "10px" },
  input: { flex: 1, padding: "12px 16px", borderRadius: "8px", border: "1px solid #333", background: "#1a1a1a", color: "#fff", fontSize: "15px" },
  sendBtn: { background: "#6c63ff", color: "#fff", border: "none", padding: "12px 24px", borderRadius: "8px", cursor: "pointer", fontWeight: "bold" },
} 