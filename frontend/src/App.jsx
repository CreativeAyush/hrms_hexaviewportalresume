import { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'

// Professional SVG Icons
const Icons = {
    Briefcase: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" /><rect width="20" height="14" x="2" y="6" rx="2" /></svg>
    ),
    Layers: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z" /><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65" /><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65" /></svg>
    ),
    BarChart: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" x2="12" y1="20" y2="10" /><line x1="18" x2="18" y1="20" y2="4" /><line x1="6" x2="6" y1="20" y2="16" /></svg>
    ),
    Settings: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" /><circle cx="12" cy="12" r="3" /></svg>
    ),
    Upload: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" x2="12" y1="3" y2="15" /></svg>
    ),
    Pen: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9" /><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" /></svg>
    ),
    FileText: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /><path d="M10 9H8" /><path d="M16 13H8" /><path d="M16 17H8" /></svg>
    ),
    Download: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" x2="12" y1="15" y2="3" /></svg>
    ),
    Eye: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" /><circle cx="12" cy="12" r="3" /></svg>
    ),
    ArrowLeft: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 19-7-7 7-7" /><path d="M19 12H5" /></svg>
    ),
    HexBrand: () => (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z" /><path d="M2 17l10 5 10-5" /><path d="M2 12l10 5 10-5" /></svg>
    )
}

function App() {
    const [file, setFile] = useState(null)
    const [customRecommendation, setCustomRecommendation] = useState('')
    const [status, setStatus] = useState('')
    const [statusType, setStatusType] = useState('')
    const [downloadUrl, setDownloadUrl] = useState('')
    const [downloadName, setDownloadName] = useState('')
    const [loading, setLoading] = useState(false)
    const [activeTab, setActiveTab] = useState('converter')
    const fileInputRef = useRef(null)

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0]
        if (selectedFile) {
            setFile(selectedFile)
            setDownloadUrl('')
            setStatus('')
            setActiveTab('converter')
        }
    }

    const handleUpload = async () => {
        if (!file) return
        const formData = new FormData()
        formData.append('file', file)
        if (customRecommendation.trim()) {
            formData.append('custom_recommendation', customRecommendation)
        }

        setLoading(true)
        setStatus('Optimizing resume document...')
        setDownloadUrl('')

        try {
            const response = await axios.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                responseType: 'blob',
            })

            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
            setDownloadUrl(url)

            const baseName = file.name.substring(0, file.name.lastIndexOf('.')) || file.name
            setDownloadName(`${baseName}.pdf`)

            setStatus('Success: Document processed.')
            setStatusType('success')
            setActiveTab('preview')
        } catch (error) {
            console.error('Error:', error)
            setStatus('System Error: Processing failed.')
            setStatusType('error')
        } finally {
            setLoading(false)
        }
    }

    const clearSession = () => {
        setFile(null)
        setDownloadUrl('')
        setStatus('')
        setCustomRecommendation('')
        setDownloadName('')
        setActiveTab('converter')
    }

    return (
        <div id="root">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="sidebar-header">
                    <div className="brand">
                        <div className="brand-icon">
                            <Icons.HexBrand />
                        </div>
                        <span className="brand-name">HEXAVIEW</span>
                    </div>
                </div>

                <nav className="nav-list">
                    <div className="nav-link active">
                        <Icons.Briefcase />
                        <span>Branding Station</span>
                    </div>
                    <div className="nav-link">
                        <Icons.Layers />
                        <span>Process Queue</span>
                    </div>
                    <div className="nav-link">
                        <Icons.BarChart />
                        <span>Analytics</span>
                    </div>
                    <div className="nav-link">
                        <Icons.Settings />
                        <span>Configurations</span>
                    </div>
                </nav>

                <div className="sidebar-footer">
                    <div className="user-card">
                        <div className="user-avatar">AD</div>
                        <div className="user-info">
                            <span className="name">Admin Dashboard</span>
                            <span className="role">Hiring Lead</span>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content Area */}
            <main className="main-content">
                <header className="header">
                    <div className="tab-switcher">
                        <button
                            className={`tab-btn ${activeTab === 'converter' ? 'active' : ''}`}
                            onClick={() => setActiveTab('converter')}
                        >
                            Branding Station
                        </button>
                        <button
                            className={`tab-btn ${activeTab === 'preview' ? 'active' : ''}`}
                            onClick={() => setActiveTab('preview')}
                            disabled={!downloadUrl}
                        >
                            Document Preview {downloadUrl && <span className="pulse-dot"></span>}
                        </button>
                    </div>
                </header>

                <section className="scroll-area">
                    {activeTab === 'converter' ? (
                        <div className="workflow-view">
                            <div className="page-header">
                                <h1>Candidate Portal</h1>
                                <p>Deliver enterprise-ready branded profiles with AI candidate insights.</p>
                            </div>

                            <div className="grid">
                                <div className="glass-card">
                                    <div className="card-header">
                                        <Icons.Upload />
                                        <h3>1. Source Selection</h3>
                                    </div>
                                    <div className="drop-zone" onClick={() => fileInputRef.current.click()}>
                                        <input
                                            type="file"
                                            ref={fileInputRef}
                                            onChange={handleFileChange}
                                            accept=".pdf,.docx"
                                            hidden
                                        />
                                        {!file ? (
                                            <>
                                                <Icons.FileText />
                                                <h4>Drop Resume</h4>
                                                <p>Upload .PDF or .DOCX format</p>
                                            </>
                                        ) : (
                                            <div className="file-pill">
                                                <div className="file-icon"><Icons.FileText /></div>
                                                <div className="file-info">
                                                    <span className="name">{file.name}</span>
                                                    <span className="size">{(file.size / 1024).toFixed(1)} KB</span>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                <div className="glass-card">
                                    <div className="card-header">
                                        <Icons.Pen />
                                        <h3>2. HR Recommendation</h3>
                                    </div>
                                    <textarea
                                        placeholder="Enter custom evaluator notes to override AI suggestions..."
                                        value={customRecommendation}
                                        onChange={(e) => setCustomRecommendation(e.target.value)}
                                    />
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="preview-container">
                            <div className="preview-nav">
                                <div className="preview-info">
                                    <h3>Interactive Preview</h3>
                                    <span className="filename">{downloadName}</span>
                                </div>
                                <div className="preview-actions">
                                    <a href={downloadUrl} download={downloadName} className="download-link">
                                        <Icons.Download />
                                        Download PDF
                                    </a>
                                    <button onClick={() => setActiveTab('converter')} className="back-btn">
                                        <Icons.ArrowLeft />
                                        Back to Station
                                    </button>
                                </div>
                            </div>
                            <div className="preview-frame">
                                <iframe src={downloadUrl} title="Document Viewer" />
                            </div>
                        </div>


                    )}
                </section>

                {activeTab === 'converter' && (
                    <footer className="actionBar">
                        <div className="status-box">
                            {status && (
                                <>
                                    {loading && <div className="spinner"></div>}
                                    <span className={statusType === 'error' ? 'error-text' : ''}>{status}</span>
                                </>
                            )}
                        </div>

                        <div className="btn-group">
                            {downloadUrl ? (
                                <>
                                    <button className="primary-btn" onClick={() => setActiveTab('preview')}>
                                        <Icons.Eye />
                                        View Branded File
                                    </button>
                                    <button className="clear-btn" onClick={clearSession}>Clear Station</button>
                                </>
                            ) : (
                                <button
                                    className="primary-btn"
                                    onClick={handleUpload}
                                    disabled={loading || !file}
                                >
                                    {loading ? 'Analyzing...' : 'Run Branding Intelligence'}
                                </button>
                            )}
                        </div>
                    </footer>
                )}
            </main>
        </div>
    )
}

export default App
