#!/bin/bash
TARGET_DIR=$(pwd)/src_code
REPORT_DIR=$(pwd)/security_reports
SONAR_URL="http://192.168.5.131:9000"
SONAR_TOKEN="sqa_5e2fb1ace586e0e2a46eea77f1b20bb4758f7c35"
PROJECT_KEY="demo_application"
mkdir -p $REPORT_DIR

echo "[*] Khởi động quét SAST với SonarScanner..."
docker run --rm \
 --network host \
 -e SONAR_HOST_URL=$SONAR_URL \
 -v $TARGET_DIR:/usr/src \
 sonarsource/sonar-scanner-cli \
 sonar-scanner \
 -Dsonar.projectKey=$PROJECT_KEY \
 -Dsonar.sources=. \
 -Dsonar.java.binaries=. \
 -Dsonar.token=$SONAR_TOKEN

echo "[*] Khởi động quét lỗ hổng nhanh với Semgrep..."
docker run --rm \
 -v $TARGET_DIR:/src \
 returntocorp/semgrep \
 semgrep scan --config "p/default" --json -o /src/semgrep_report.json /src
mv $TARGET_DIR/semgrep_report.json $REPORT_DIR/

echo "[*] Khởi động quét phân tích thành phần (SCA) với OWASP Dependency Check..."
docker run --rm \
 -u $(id -u ${USER}):$(id -g ${USER}) \
 -v $TARGET_DIR:/src:z \
 -v $REPORT_DIR:/report:z \
 -v dependency-check-data:/usr/share/dependency-check/data \
 owasp/dependency-check:latest \
 --scan /src \
 --format JSON \
 --format HTML \
 --out /report \
 --project "$PROJECT_KEY"
