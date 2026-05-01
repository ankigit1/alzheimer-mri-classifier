# Alzheimer Dementia Classification System

## 🧠 Overview

An advanced **AI-powered medical diagnosis system** for detecting and classifying Alzheimer's dementia stages from brain MRI scans. Features Siamese Capsule Networks with 99% accuracy using clinical-grade validation.

**Status**: ✅ Production Ready | 🔧 Fully Tested | 📊 SNNCap V2.0 Support

---

## ✨ Features

- **🎯 AI Model**: SNNCap V2.0 (99% acc, upgraded version)
- **💻 Modern Web UI**: React + Vite + Tailwind CSS with professional design
- **⚡ FastAPI Backend**: High-performance async inference with Uvicorn
- **📊 Real-time Analysis**: Process MRI scans in seconds
- **📝 Request Logging**: Request IDs, timing metrics, and audit trail
- **🔐 Secure Processing**: Proper input validation and error handling
- **🎨 Responsive Design**: Works on desktop, tablet, and mobile
- **📈 4-Class Classification**:
  - No Dementia (Non-Demented)
  - Very Mild Dementia
  - Mild Dementia
  - Moderate Dementia

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│                                                             │
│  React + Vite (Port 3000)                                  │
│  ├── File Upload (Drag & Drop)                            │
│  ├── SNNCap V2.0 Model                                    │
│  ├── Real-time Analysis Results                           │
│  └── Confidence Visualization (Bar Charts)                │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP REST API
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    Backend Layer                           │
│                                                            │
│  FastAPI (Port 5000)                                       │
│  ├── /health → Server status                             │
│  ├── /models → Available models                          │
│  └── /analyse_mri → MRI analysis (file + model_version)  │
│                                                            │
│  Request Logging Middleware                              │
│  └── Logs all requests with IDs and timing              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│              Inference & Model Layer                       │
│                                                            │
│  ModelRegistry (Lazy Loading)                            │
│  └── SNNCap_v2.0/                                        │
│      ├── siamese_capsule_finetuned.pth                  │
│      └── reference_embeddings_means_finetuned.pt        │
│                                                            │
│  PyTorch Models                                          │
│  └── Siamese Capsule Network (4-class)                  │
└────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Windows 10+
- Python 3.10+
- Node.js 18+
- npm

### Installation & Run

**One-Command Startup:**
```powershell
cd e:\projectWork\API
.\start.ps1
```

This automatically:
1. ✅ Creates Python virtual environment
2. ✅ Installs Python dependencies
3. ✅ Installs Node.js packages
4. ✅ Starts FastAPI backend (port 5000)
5. ✅ Starts React dev server (port 3000)
6. ✅ Opens browsers for both services

**Access Points:**
- 🌐 **UI**: http://localhost:3000/
- 📡 **API**: http://localhost:5000/
- ✅ **Health Check**: http://localhost:5000/health

---

## 📚 API Endpoints

### 1. Health Check
```http
GET /health

Response:
{
  "status": "ok"
}
```

### 2. List Available Models
```http
GET /models

Response:
{
  "models": [
    "SNNCap V2.0"
  ]
}
```

### 3. Analyze MRI Scan
```http
POST /analyse_mri

Content-Type: multipart/form-data
Body:
  - file: <MRI image file (PNG/JPG)>
  - model_version: "SNNCap V2.0" (default: V2.0)

Response:
{
  "model_version": "SNNCap V2.0",
  "predicted_class": "Mild Dementia",
  "closeness": {
    "No Dementia": 15.23,
    "Very Mild Dementia": 25.67,
    "Mild Dementia": 48.92,
    "Moderate Dementia": 10.18
  },
  "distances": [3.45, 2.89, 1.23, 4.12]
}
```

---

## 📁 Project Structure

```
E:\projectWork\API/
├── 📄 README.md                    ← You are here
├── 📄 requirements.txt             ← Python dependencies
├── 🔧 start.ps1                    ← Startup script (PowerShell)
│
├── 📁 api/                         ← FastAPI Backend
│   ├── app.py                      ← Main FastAPI app
│   ├── inference.py                ← Model inference logic
│   ├── middleware.py               ← Request logging middleware
│   └── __init__.py
│
├── 📁 alz-frontend-main/           ← React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Index.jsx           ← Main page with model selector
│   │   │   └── NotFound.jsx
│   │   ├── components/
│   │   │   ├── MRIUpload.jsx       ← File upload + results
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── ui/                 ← shadcn UI components
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tsconfig.json
│
├── 📁 logger/                      ← Logging System
│   └── logger.py                   ← Centralized logging config
│
├── 📁 logs/                        ← Log Files
│   ├── start.log                   ← Startup logs
│   └── inference.log               ← API & inference logs
│
├── 📁 SNNCap_v2.0/                 ← Model V2.0 Artifacts
│   ├── siamese_capsule_finetuned.pth
│   └── reference_embeddings_means_finetuned.pt
│
├── 📁 notebooks/                   ← Training & Analysis
│   └── snncap_training.ipynb
│
└── 📁 data/                        ← Dataset Storage
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (async web framework)
- **Server**: Uvicorn (ASGI server)
- **Model**: PyTorch (deep learning)
- **Logging**: Python logging with rotating file handlers

### Frontend
- **Framework**: React 18 (UI library)
- **Build Tool**: Vite (fast dev server)
- **Styling**: Tailwind CSS (utility-first CSS)
- **Components**: shadcn/ui (accessible UI components)
- **Charts**: Recharts (data visualization)
- **Forms**: React Hook Form (form management)
- **Notifications**: Sonner (toast notifications)

### DevOps
- **Language**: PowerShell (automation)
- **Environment**: Python venv (isolation)
- **Package Manager**: npm (dependencies)

---

---

## 📊 Logs & Monitoring

### Log Files
- **`logs/start.log`**: Startup sequence, dependency installation
- **`logs/inference.log`**: API requests, model inference, errors

### View Recent Logs
```powershell
# Last 50 lines of inference log
Get-Content -Path "logs/inference.log" -Tail 50

# Monitor logs in real-time
Get-Content -Path "logs/inference.log" -Wait
```

---

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Find process using port 3000
Get-NetTCPConnection -LocalPort 3000

# Kill the process
Stop-Process -Id <PID> -Force

# Try startup again
.\start.ps1
```

### React Page Not Loading
1. Hard refresh browser: **Ctrl+Shift+R**
2. Clear cache: **Ctrl+Shift+Delete**
3. Check browser console for errors: **F12**

### API Connection Error
1. Verify API is running: `http://localhost:5000/health`
2. Check firewall settings
3. Review logs: `logs/inference.log`

### Model Loading Error
1. Verify model files exist in `SNNCap_v2.0/`
2. Check `logs/inference.log` for details
3. Restart with: `.\start.ps1`

---

## 🔐 Security & Privacy

- ✅ Input validation on file uploads
- ✅ Secure image processing (PIL)
- ✅ Request ID tracking for audit trail
- ✅ Error handling without data leakage
- ✅ Proper CORS handling
- ✅ Model inference isolated from user data

---

## 📈 Performance

- **Inference Time**: ~500-600ms (V2.0)
- **Memory Usage**: ~2-3GB with models loaded
- **Concurrent Requests**: Handle multiple simultaneous uploads
- **Startup Time**: ~30 seconds (includes model loading)

---

## 🤝 Contributing

To modify or extend the project:

1. **Backend Changes**: Edit `api/app.py` or `api/inference.py`
2. **Frontend Changes**: Edit `alz-frontend-main/src/`
2. **Models**: Replace `.pth` files in `SNNCap_v2.0/`
4. **Logging**: Modify `logger/logger.py`
---

## 📚 Research & Credits

**Research Paper**: [IEEE Xplore - Siamese Capsule Networks for Alzheimer's Classification](https://ieeexplore.ieee.org/abstract/document/11488457)

**Built and Deployed by**: Ankit Garg
### Hot Reload During Development
- **Frontend**: Changes auto-reload in browser (Vite HMR)
- **Backend**: Manual restart of `start.ps1` required

---

## 📝 Notes

- This system is designed for **screening and clinical support only**
- Always consult medical professionals for diagnosis
- Patient data should be handled according to HIPAA/GDPR regulations
- Model predictions are probabilistic, not definitive

---

## 📞 Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages in browser console
3. Verify all services are running
4. Restart with fresh `.\start.ps1`

---

**Last Updated**: April 28, 2026  
**Status**: ✅ Production Ready  
**Version**: 2.0
