import requests
import os

# ================== CẤU HÌNH THEO TÀI LIỆU ==================
DOJO_API_URL = "http://localhost:8080/api/v2/reimport-scan/"
API_TOKEN = "d170aea19d1626daa697476b7c89a21cfd01125d"   # ← THAY BẰNG TOKEN THẬT CỦA BẠN
ENGAGEMENT_ID = 1

def upload_scan_report(file_path, scan_type):
    if not os.path.exists(file_path):
        print(f"[-] Không tìm thấy tệp báo cáo: {file_path}")
        return

    headers = {
        'Authorization': f'Token {API_TOKEN}'
    }

    data = {
        'engagement': ENGAGEMENT_ID,
        'scan_type': scan_type,
        'active': True,
        'verified': False,
        'minimum_severity': 'Info'
    }

    with open(file_path, 'rb') as f:
        files = {'file': f}
        print(f"[*] Tiến hành đẩy dữ liệu quét '{scan_type}'...")
        response = requests.post(DOJO_API_URL, headers=headers, data=data, files=files)

        if response.status_code in [201, 200]:
            print(f"[+] Nhập dữ liệu thành công cho {scan_type}.")
        else:
            print(f"[-] Quá trình nhập thất bại. Mã lỗi: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    REPORT_DIR = "security_reports"
    
    reports = [
        (f"{REPORT_DIR}/semgrep_report.json", "Semgrep JSON Report"),
        (f"{REPORT_DIR}/dependency-check-report.json", "OWASP Dependency Check"),
        # SonarQube đã được upload trực tiếp qua scanner → DefectDojo dùng parser "SonarQube API Import"
    ]

    print("[*] Bắt đầu tự động nhập báo cáo vào DefectDojo...")
    for file_path, scan_type in reports:
        upload_scan_report(file_path, scan_type)
    
    print("[✔] Hoàn tất nhập liệu vào DefectDojo!")
