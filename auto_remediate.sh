#!/bin/bash
echo "[*] Bắt đầu Auto Remediation bằng Cline (Agentic AI)..."

# Chạy Cline với prompt tự động khắc phục lỗ hổng
cline -y ask "
Bạn là kỹ sư DevSecOps chuyên nghiệp.
Hãy sử dụng MCP 'defectdojo' để:
1. Lấy danh sách lỗ hổng High/Critical
2. Phân tích và đề xuất cách vá code
3. Thực hiện vá tự động nếu có thể
"

echo "[✓] Hoàn thành Auto Remediation!"
