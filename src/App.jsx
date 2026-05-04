function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect x="2" y="6" width="28" height="20" rx="2" stroke="currentColor" strokeWidth="2"/>
              <path d="M8 12h16M8 16h12M8 20h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            <span className="logo-text">Slidr</span>
          </div>
          <nav className="nav">
            <a href="#features">Features</a>
            <a href="#templates">Templates</a>
            <a href="#installation">Installation</a>
            <a href="https://github.com/blastbraker/Slidr" target="_blank" rel="noopener noreferrer" className="github-link">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.75-1.41-.76-1.695-.42-.345-1.59-.48-1.83-.465-.24.015-1.26.195-1.8.75C6.255 8.355 6.63 7.5 6.63 7.5c-.45-1.305.315-1.44.315-1.44-1.395-.18.09-1.425.09-1.425 1.545-.15 2.205 1.185 2.205 1.185 1.38 2.205 3.69 1.665 4.545 1.41.105-.855.45-1.44.81-1.77-3.51-.39-7.2-1.755-7.2-7.815 0-1.71.615-3.12 1.62-4.215-.165-.405-.705-1.995.15-4.155 0 0 1.32-.42 4.335 1.605C9.735 2.49 10.86 2.49 12 2.49c1.14 0 2.265.015 3.3.045 3.015-2.025 4.335-1.605 4.335-1.605.855 2.16.315 3.75.15 4.155 1.005 1.095 1.62 2.505 1.62 4.215 0 6.075-3.69 7.425-7.215 7.8.555.48 1.065 1.425 1.065 2.88 0 2.085-.015 3.77-.015 4.27 0 .315.225.675.825.57C20.565 21.795 24 17.31 24 12c0-6.63-5.37-12-12-12z"/>
              </svg>
              GitHub
            </a>
          </nav>
        </div>
      </header>

      <section className="hero">
        <div className="hero-content">
          <h1>AI Presentation Maker</h1>
          <p className="tagline">Create professional presentations from topics or documents using AI. Supports PPTX, PDF, and web-based HTML output.</p>
          <div className="hero-buttons">
            <a href="#installation" className="btn btn-primary">Get Started</a>
            <a href="https://github.com/blastbraker/Slidr" target="_blank" rel="noopener noreferrer" className="btn btn-secondary">View on GitHub</a>
          </div>
        </div>
      </section>

      <section id="features" className="features">
        <div className="section-content">
          <h2>Features</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                  <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
                </svg>
              </div>
              <h3>Multiple Input Methods</h3>
              <p>Enter a topic directly or upload PDF/DOCX files</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2a10 10 0 100 20 10 10 0 000-20z"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <h3>AI-Powered</h3>
              <p>Generate slide content using local Ollama AI</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
                </svg>
              </div>
              <h3>Multiple Outputs</h3>
              <p>Export to PPTX, PDF, and HTML formats</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <path d="M3 9h18M9 21V9"/>
                </svg>
              </div>
              <h3>Custom Templates</h3>
              <p>Choose from 3 built-in themes (Minimal, Modern, Corporate)</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <h3>100% Free</h3>
              <p>Uses local Ollama AI - no API costs</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2"/>
                  <path d="M8 21h8M12 17v4"/>
                </svg>
              </div>
              <h3>Cross-Platform</h3>
              <p>Works on Windows, macOS, and Linux</p>
            </div>
          </div>
        </div>
      </section>

      <section id="templates" className="templates">
        <div className="section-content">
          <h2>Templates</h2>
          <div className="templates-grid">
            <div className="template-card minimal">
              <div className="template-preview">
                <div className="template-slide">
                  <div className="slide-accent"></div>
                  <div className="slide-content">
                    <div className="slide-title">Title</div>
                    <div className="slide-lines">
                      <div></div><div></div><div></div>
                    </div>
                  </div>
                </div>
              </div>
              <h3>Minimal</h3>
              <p>Clean modern look with accent colors</p>
            </div>
            <div className="template-card modern">
              <div className="template-preview">
                <div className="template-slide dark">
                  <div className="slide-accent"></div>
                  <div className="slide-content">
                    <div className="slide-title">Title</div>
                    <div className="slide-lines">
                      <div></div><div></div><div></div>
                    </div>
                  </div>
                </div>
              </div>
              <h3>Modern</h3>
              <p>Dark theme with accent bar</p>
            </div>
            <div className="template-card corporate">
              <div className="template-preview">
                <div className="template-slide corporate-theme">
                  <div className="slide-accent"></div>
                  <div className="slide-content">
                    <div className="slide-title">Title</div>
                    <div className="slide-lines">
                      <div></div><div></div><div></div>
                    </div>
                  </div>
                </div>
              </div>
              <h3>Corporate</h3>
              <p>Professional blue/gray</p>
            </div>
          </div>
        </div>
      </section>

      <section id="installation" className="installation">
        <div className="section-content">
          <h2>Installation</h2>
          <div className="installation-steps">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Clone the Repository</h3>
                <pre><code>git clone https://github.com/blastbraker/Slidr.git
cd Slidr</code></pre>
              </div>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Install Ollama</h3>
                <p>Download from <a href="https://ollama.com" target="_blank" rel="noopener noreferrer">ollama.com</a> and install for your OS.</p>
                <pre><code>ollama pull llama3.2:3b</code></pre>
              </div>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Install Python Dependencies</h3>
                <pre><code>pip install -r requirements.txt</code></pre>
              </div>
            </div>
            <div className="step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>Run Slidr</h3>
                <pre><code>python -m slidr.gui</code></pre>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-links">
            <a href="https://github.com/blastbraker/Slidr" target="_blank" rel="noopener noreferrer">GitHub</a>
            <a href="https://github.com/blastbraker/Slidr/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">License</a>
          </div>
          <p className="copyright">MIT License &middot; Built by <a href="https://github.com/blastbraker" target="_blank" rel="noopener noreferrer">Ali Bahar</a></p>
        </div>
      </footer>
    </div>
  )
}

export default App