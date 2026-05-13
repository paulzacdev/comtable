import os
from fastapi import FastAPI, UploadFile, File
from agents.collector import collector
from agents.auditor import auditor
from agents.analyst import analyst
from core.main import app

@app.post("/api/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):
    # Simulate OCR processing (In production, use pytesseract or PaddleOCR here)
    content = await file.read()
    simulated_text = f"Invoice INV-2026-001. Date: 2026-05-13. Total: 1200 USD. Tax: 200 USD. Vendor: TechCorp Inc."

    # 1. Collector Agent extracts and categorizes
    extracted = collector.extract_data(simulated_text)
    category = collector.categorize_document(extracted)

    # 2. Auditor Agent checks for anomalies
    anomaly_check = auditor.check_anomalies([{"data": extracted}])

    return {
        "filename": file.filename,
        "extracted_data": extracted,
        "category": category,
        "audit_report": anomaly_check
    }

@app.get("/api/system-health")
async def get_health():
    return {"status": "online", "agents": ["collector", "auditor", "analyst", "operator"]}
