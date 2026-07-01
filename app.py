from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib

# 1. Initialize the FastAPI application (This is the 'app' that was missing!)
app = FastAPI(title="PhishGuard API", description="AI-powered Phishing URL Detector")

# 2. Load the trained AI model
model = joblib.load("phishing_model.pkl")

# 3. Create a data rule
class URLRequest(BaseModel):
    url: str

def extract_features_from_string(url: str):
    url_length = len(url)
    dot_count = url.count('.')
    has_at_symbol = 1 if '@' in url else 0
    is_https = 1 if url.startswith("https") else 0
    return [[url_length, dot_count, has_at_symbol, is_https]]

# 4. The Prediction API Endpoint
@app.post("/predict")
def predict_url(request: URLRequest):
    raw_url = request.url
    numeric_features = extract_features_from_string(raw_url)
    
    prediction = model.predict(numeric_features)[0]
    probabilities = model.predict_proba(numeric_features)[0]
    phishing_probability = float(probabilities[1]) 
    
    result_status = "Phishing / Malicious" if prediction == 1 else "Safe / Benign"
    
    return {
        "url_analyzed": raw_url,
        "status": result_status,
        "phishing_risk_score_percentage": round(phishing_probability * 100, 2)
    }

# 5. The Advanced Cyber-Theme Frontend
@app.get("/", response_class=HTMLResponse)
def home_frontend():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PhishGuard AI | Threat Intelligence</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Space+Mono:ital,wght@0,400;0,700&display=swap');
            
            body {
                background-color: #050b14;
                background-image: 
                    radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                    radial-gradient(at 50% 0%, hsla(225,39%,30%,0.1) 0, transparent 50%), 
                    radial-gradient(at 100% 0%, hsla(339,49%,30%,0.1) 0, transparent 50%);
                font-family: 'Space Mono', monospace;
                color: #e2e8f0;
            }
            .glass-panel {
                background: rgba(15, 23, 42, 0.6);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }
            .cyber-input {
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid #334155;
                transition: all 0.3s ease;
            }
            .cyber-input:focus {
                border-color: #3b82f6;
                box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
                outline: none;
            }
            .scan-line {
                width: 100%;
                height: 2px;
                background: #3b82f6;
                position: absolute;
                top: 0;
                left: 0;
                animation: scan 1.5s infinite linear;
                box-shadow: 0 0 10px #3b82f6;
                display: none;
            }
            @keyframes scan {
                0% { top: 0; opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { top: 100%; opacity: 0; }
            }
            .glow-text {
                font-family: 'Orbitron', sans-serif;
                text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
            }
        </style>
    </head>
    <body class="min-h-screen flex flex-col justify-center items-center p-4 relative overflow-hidden">
        
        <div class="absolute inset-0 z-0 opacity-[0.03]" 
             style="background-image: linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px); background-size: 30px 30px;">
        </div>

        <div class="glass-panel w-full max-w-2xl p-8 rounded-2xl z-10 relative overflow-hidden">
            <div id="scannerLine" class="scan-line"></div>
            
            <div class="text-center mb-8">
                <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-900/30 text-blue-500 mb-4 border border-blue-500/30">
                    <i class="fa-solid fa-shield-halved text-2xl"></i>
                </div>
                <h1 class="text-4xl font-bold glow-text text-white tracking-wider">PHISHGUARD<span class="text-blue-500">_AI</span></h1>
                <p class="text-slate-400 mt-2 text-sm uppercase tracking-widest">Neural Network Threat Detection</p>
            </div>
            
            <div class="space-y-6">
                <div class="relative">
                    <i class="fa-solid fa-link absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-500"></i>
                    <input id="urlInput" type="text" placeholder="Enter target URL for deep scan..." 
                           class="cyber-input w-full py-4 pl-12 pr-4 rounded-xl text-white placeholder-slate-600 font-mono text-sm tracking-wide">
                </div>
                
                <button onclick="triggerScan()" id="scanBtn"
                        class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-[1.02] shadow-[0_0_20px_rgba(59,130,246,0.4)] flex items-center justify-center gap-3">
                    <i id="btnIcon" class="fa-solid fa-radar text-lg"></i>
                    <span id="btnText" class="tracking-widest uppercase">Initiate AI Scan</span>
                </button>
            </div>

            <div id="loadingState" class="hidden mt-8 text-center">
                <i class="fa-solid fa-circle-notch fa-spin text-blue-500 text-3xl mb-3"></i>
                <p class="text-blue-400 text-sm animate-pulse">Extracting features & querying Random Forest model...</p>
            </div>

            <div id="resultBox" class="mt-8 hidden opacity-0 transition-opacity duration-500">
                <div class="border-t border-slate-700/50 pt-6">
                    <div class="flex justify-between items-end mb-4">
                        <h3 class="text-slate-400 text-xs uppercase tracking-widest">Analysis Report</h3>
                        <span id="resVerdictBadge" class="px-3 py-1 rounded-full text-xs font-bold border"></span>
                    </div>
                    
                    <div class="bg-black/40 rounded-lg p-4 border border-slate-800 mb-6 break-all">
                        <p class="text-xs text-slate-500 mb-1">TARGET_URL:</p>
                        <p id="resUrl" class="text-blue-300 text-sm"></p>
                    </div>

                    <div class="space-y-2">
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-400">Threat Probability:</span>
                            <span id="resScoreText" class="font-bold"></span>
                        </div>
                        <div class="w-full bg-slate-800 rounded-full h-3 overflow-hidden border border-slate-700">
                            <div id="resScoreBar" class="h-full rounded-full transition-all duration-1000 w-0"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function triggerScan() {
                const urlVal = document.getElementById('urlInput').value.trim();
                if(!urlVal) {
                    document.getElementById('urlInput').classList.add('border-red-500');
                    setTimeout(() => document.getElementById('urlInput').classList.remove('border-red-500'), 1000);
                    return;
                }
                
                // UI State: Scanning
                const btn = document.getElementById('scanBtn');
                const btnIcon = document.getElementById('btnIcon');
                const btnText = document.getElementById('btnText');
                const scannerLine = document.getElementById('scannerLine');
                const loading = document.getElementById('loadingState');
                const resultBox = document.getElementById('resultBox');

                // Reset UI
                resultBox.classList.add('hidden');
                resultBox.classList.remove('opacity-100');
                document.getElementById('resScoreBar').style.width = '0%';
                
                btn.disabled = true;
                btn.classList.replace('bg-blue-600', 'bg-slate-700');
                btn.classList.remove('shadow-[0_0_20px_rgba(59,130,246,0.4)]', 'hover:scale-[1.02]');
                btnIcon.className = "fa-solid fa-lock text-slate-400";
                btnText.innerText = "CONNECTION SECURED";
                scannerLine.style.display = 'block';
                loading.classList.remove('hidden');

                try {
                    // Simulate a deep-scan delay for dramatic effect (1.5 seconds)
                    await new Promise(r => setTimeout(r, 1500));

                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ url: urlVal })
                    });
                    const data = await response.json();
                    
                    // Populate Data
                    document.getElementById('resUrl').innerText = data.url_analyzed;
                    document.getElementById('resScoreText').innerText = data.phishing_risk_score_percentage + "%";
                    
                    const badge = document.getElementById('resVerdictBadge');
                    const scoreBar = document.getElementById('resScoreBar');
                    const isPhishing = data.status.includes("Phishing");

                    if(isPhishing) {
                        badge.innerText = "CRITICAL THREAT DETECTED";
                        badge.className = "px-3 py-1 rounded-full text-xs font-bold border border-red-500 bg-red-900/30 text-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]";
                        scoreBar.className = "h-full rounded-full transition-all duration-1000 bg-gradient-to-r from-red-600 to-red-400";
                        document.getElementById('resScoreText').className = "font-bold text-red-400";
                    } else {
                        badge.innerText = "NETWORK SECURE";
                        badge.className = "px-3 py-1 rounded-full text-xs font-bold border border-emerald-500 bg-emerald-900/30 text-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]";
                        scoreBar.className = "h-full rounded-full transition-all duration-1000 bg-gradient-to-r from-emerald-600 to-emerald-400";
                        document.getElementById('resScoreText').className = "font-bold text-emerald-400";
                    }

                    // Reveal Result
                    loading.classList.add('hidden');
                    resultBox.classList.remove('hidden');
                    
                    // Trigger reflow to ensure transition runs, then set width
                    void resultBox.offsetWidth; 
                    resultBox.classList.add('opacity-100');
                    setTimeout(() => {
                        scoreBar.style.width = data.phishing_risk_score_percentage + "%";
                    }, 100);

                } catch(err) {
                    alert("API Connection Error. Verify FastAPI server is running.");
                    loading.classList.add('hidden');
                } finally {
                    // Reset Button
                    btn.disabled = false;
                    btn.classList.replace('bg-slate-700', 'bg-blue-600');
                    btn.classList.add('shadow-[0_0_20px_rgba(59,130,246,0.4)]', 'hover:scale-[1.02]');
                    btnIcon.className = "fa-solid fa-radar text-lg text-white";
                    btnText.innerText = "INITIATE AI SCAN";
                    scannerLine.style.display = 'none';
                }
            }
        </script>
    </body>
    </html>
    """