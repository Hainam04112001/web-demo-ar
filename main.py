from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="WebAR Backend API",
    version="1.0.0"
)

# Cấu hình CORS để cho phép điện thoại kết nối từ xa trong mạng nội bộ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ARScanRequest(BaseModel):
    target_id: str
    device_type: str

# Trả về trực tiếp file HTML tĩnh cho cả PC và điện thoại
@app.get("/")
async def render_ar_page():
    file_path = os.path.join("templates", "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"error": "Không tìm thấy file index.html trong thư mục templates!"})

# API ghi nhận khi thiết bị quét thành công
@app.post("/api/scan")
async def record_ar_scan(data: ARScanRequest):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Đã quét thành công - Target: {data.target_id} | Device: {data.device_type}")
    return {"status": "success", "target_id": data.target_id, "time": timestamp}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)