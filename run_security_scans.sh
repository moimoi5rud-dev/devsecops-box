cat << 'EOF' > run_security_scans.sh
#!/bin/bash
TARGET_DIR=$(pwd)/src_code
REPORT_DIR=$(pwd)/security_reports
SONAR_URL="http://localhost:9000"
SONAR_TOKEN="sqp_8a1b2c3d4e5f6g7h8i9j0k"
PROJECT_KEY="demo_application"

mkdir -p $REPORT_DIR

echo "[*] Khởi động quét SAST với SonarScanner..."
docker run --rm \
    -e SONAR_HOST_URL=$SONAR_URL \
    -e SONAR_LOGIN=$SONAR_TOKEN \
    -v $TARGET_DIR:/usr/src \
    sonarsource/sonar-scanner-cli \
    sonar-scanner \
    -Dsonar.projectKey=$PROJECT_KEY \
    -Dsonar.sources=. \
    -Dsonar.java.binaries=.

echo "[*] Khởi động quét lỗ hổng nhanh với Semgrep..."
docker run --rm \
    -v $TARGET_DIR:/src \
    returntocorp/semgrep \
    semgrep scan --config "p/default" --json -o /src/semgrep_report.json /src

mv $TARGET_DIR/semgrep_report.json $REPORT_DIR/ 2>/dev/null || true

echo "[*] Khởi động quét phân tích thành phần (SCA) với OWASP Dependency-Check..."
docker run --rm \
    -e user=$USER \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    -v $TARGET_DIR:/src:z \
    -v $REPORT_DIR:/report:z \
    owasp/dependency-check:latest \
    --scan /src \
    --format JSON \
    --out /report \
    --project "$PROJECT_KEY" \
    --noupdate
EOF
