# TrustChain AI

AI-Assisted Document Verification & Fraud Analysis Platform

---

## Overview

TrustChain AI is a full-stack intelligent document verification platform designed to analyze, classify, verify, and generate trust reports for uploaded digital documents.

The platform combines:

- OCR (Optical Character Recognition)
- Fraud Analysis
- Document Intelligence Extraction
- QR-Based Public Verification
- Verification Reports
- Dashboard Analytics

to create a unified document trust workflow system.

---

# Features

## Authentication System

- User Signup
- User Login
- JWT Authentication
- Protected Routes
- Persistent Login State
- Logout Functionality

---

## Intelligent Document Upload

- Drag & Drop Upload
- PDF Support
- Image Support
- Upload Preview
- Processing Animations
- Protected Upload Workflow

---

## OCR & Extraction Engine

The platform extracts and analyzes information from:

- PAN Cards
- Aadhaar Cards
- Passports
- Invoices
- Resumes
- Bank Statements
- Academic Certificates
- Driving Licenses
- Voter IDs

### Extracted Fields

- PAN Number
- Aadhaar Number
- Passport Number
- Nationality
- Expiry Date
- Invoice Number
- Total Amount
- Email
- Phone Number
- Skills
- IFSC Code
- Account Number
- Bank Name
- University Name
- CGPA
- Voter ID

---

# Fraud Detection System

Current fraud analysis includes:

- Metadata Inspection
- Photoshop/Canva Detection
- OCR Quality Analysis
- Missing Field Detection
- Structural Heuristics
- Confidence Scoring

---

# Dashboard Analytics

The dashboard includes:

- Upload History
- Fraud Detection Trends
- Verification Statistics
- Reports Management
- Analytics Overview

---

# PDF Verification Reports

Generated reports include:

- Fraud Risk
- Confidence Score
- Extracted Intelligence
- QR Verification Code
- Verification Status
- Document Hash

---

# QR Public Verification

Each generated report contains a QR code.

Users can:
- Scan the QR
- Open public verification page
- Validate document verification status

---

# Tech Stack

## Frontend

- React
- React Router DOM
- Tailwind CSS
- Recharts

## Backend

- FastAPI
- Python
- PyTesseract
- pdf2image
- Pillow
- ReportLab
- qrcode

## Database

- MongoDB

---

# System Architecture

```text
Upload Document
        ↓
OCR Extraction
        ↓
Document Classification
        ↓
Field Extraction
        ↓
Fraud Analysis
        ↓
Confidence Scoring
        ↓
PDF Report Generation
        ↓
QR Verification
```

---

# Project Structure

```bash
trustchain-ai/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── context/
│
├── backend/
│   ├── main.py
│   ├── reports/
│   ├── qr_codes/
│   └── requirements.txt
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <your-repo-url>
cd trustchain-ai
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# Environment Variables

Create a `.env` file inside backend:

```env
MONGO_URI=your_mongodb_uri
JWT_SECRET=your_secret_key
```

---

# Current Capabilities

- OCR Extraction
- Multi-Document Support
- Fraud Heuristics
- Dashboard Analytics
- PDF Reports
- QR Verification
- Authentication System
- Upload Workflow
- Intelligent Extraction

---

# Future Roadmap

- ML-Based Fraud Detection
- OpenCV Tampering Detection
- Layout Verification AI
- Blockchain Verification
- Cloud Storage
- Deployment
- Computer Vision Analysis
- Signature Verification
- Face Matching

---

# Current Limitations

This project is currently:

- AI-assisted verification workflow platform
- Not a government-grade forensic authenticity engine
- Not connected to official issuer databases

---

# Author

Developed by Raj

---

# License

This project is for educational and research purposes.
