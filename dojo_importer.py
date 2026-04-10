import requests
import sys
import os

# ================== CẤU HÌNH QUA GITHUB SECRETS ==================
DOJO_API_URL = os.getenv("DOJO_API_URL", "http://localhost:8080/api/v2/reimport-scan/")
API_TOKEN = os.getenv("DEFECTDOJO_API_TOKEN")
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

        if response.status_code in (200, 201):
            print(f"[+] Nhập dữ liệu thành công cho {scan_type}.")
        else:
            print(f"[-] Quá trình nhập thất bại. Mã lỗi: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    reports = [
        ("security_reports/semgrep_report.json", "Semgrep JSON Report"),
        ("security_reports/dependency-check-report.json", "OWASP Dependency-Check"),
    ]

    print("[*] Bắt đầu tự động nhập báo cáo vào DefectDojo...")
    for file_path, scan_type in reports:
        upload_scan_report(file_path, scan_type)

    print("[✓] Hoàn tất nhập liệu vào DefectDojo!")
