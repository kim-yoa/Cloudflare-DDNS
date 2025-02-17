## Cloudflare DDNS Updater

이 프로젝트는 Cloudflare API를 사용하여 사용자의 공인 IP 주소를 주기적으로 확인하고, 해당 IP 주소를 Cloudflare DNS 레코드에 자동으로 업데이트하는 파이썬 스크립트입니다. 동적 IP 주소를 사용하는 환경에서 Cloudflare를 통해 호스팅되는 도메인의 DNS 레코드를 자동으로 관리할 수 있습니다.

### 주요 기능

*   **자동 IP 주소 확인:** 스크립트는 설정된 간격으로 사용자의 공인 IP 주소를 확인합니다.
*   **Cloudflare DNS 레코드 업데이트:** IP 주소가 변경되면 Cloudflare API를 사용하여 해당 DNS 레코드를 업데이트합니다.
*   **설정 파일 관리:** API 토큰, Zone ID, 레코드 이름 등의 설정은 외부 YAML 파일로 관리되어 코드에서 분리됩니다.
*   **클래스 기반 구조:** 코드는 클래스 기반으로 구성되어 가독성과 유지보수성이 높습니다.
*   **로깅:** 스크립트의 동작 상태를 콘솔에 출력하여 디버깅 및 모니터링을 용이하게 합니다.

### 필수 구성 요소

*   **Python 3.6 이상**
*   **pip**: Python 패키지 관리자
*   **필요한 라이브러리**:
    *   requests
    *   PyYAML

### 설치 방법

1.  **Python 설치:** Python이 설치되어 있지 않다면, [Python 공식 웹사이트](https://www.python.org/)에서 최신 버전을 다운로드하여 설치합니다. 설치 시 "Add Python to PATH" 옵션을 반드시 선택하세요.
2.  **저장소 복제:** GitHub 저장소를 복제합니다.

    ```bash
    git clone https://github.com/kim-yoa/Cloudflare-DDNS.git
    cd [프로젝트 디렉토리]
    ```

3.  **필수 라이브러리 설치:** `pip`를 사용하여 필요한 라이브러리를 설치합니다.


    ```bash
    pip install requests pyyaml
    ```

4.  **설정 파일 생성:** `config.example.yml` 파일을 복사하여 `config.yml` 파일을 생성하고, 필요한 설정을 입력합니다.

    ```bash
    cp config.example.yml config.yml
    ```

    `config.yml` 파일의 내용은 다음과 같습니다.

    ```yaml
    cloudflare:
      api_token: "YOUR_CLOUDFLARE_API_TOKEN"  # Cloudflare API 토큰
      zone_id: "YOUR_ZONE_ID"                  # Cloudflare Zone ID
      record_name: "YOUR_DOMAIN"          # 업데이트할 DNS 레코드 이름

    ip_check:
      api_url: "https://api.ip.pe.kr/"        # IP 주소 확인 API URL

    settings:
      interval: 1800                          # IP 주소 확인 간격 (초 단위, 기본값: 1800초 = 30분)
      proxied: false                          # Cloudflare 프록시 사용 여부 (true 또는 false)
    ```

    *   `api_token`: Cloudflare API 토큰을 입력합니다.
    *   `zone_id`: Cloudflare Zone ID를 입력합니다.
    *   `record_name`: 업데이트할 DNS 레코드 이름을 입력합니다.
    *   `api_url`: IP 주소를 확인할 API URL을 입력합니다. 기본값은 `https://api.ip.pe.kr/`입니다.
    *   `interval`: IP 주소를 확인할 간격을 초 단위로 입력합니다. 기본값은 1800초(30분)입니다.
    *   `proxied`: Cloudflare 프록시를 사용할지 여부를 설정합니다. `true` 또는 `false` 값을 입력합니다.

5.  **스크립트 실행:** 다음 명령어를 사용하여 스크립트를 실행합니다.

    ```bash
    python ddns_updater.py
    ```

### 설정

*   **`config.yml` 파일:**
    *   `cloudflare.api_token`: Cloudflare API 토큰을 설정합니다. Cloudflare 대시보드에서 API 토큰을 생성할 수 있습니다.
    *   `cloudflare.zone_id`: Cloudflare Zone ID를 설정합니다. Cloudflare 대시보드에서 Zone ID를 확인할 수 있습니다.
    *   `cloudflare.record_name`: 업데이트할 DNS 레코드 이름을 설정합니다.
    *   `ip_check.api_url`: IP 주소를 확인할 API URL을 설정합니다. 기본 API 외 다른 IP 확인 API를 사용할 수 있습니다.
    *   `settings.interval`: IP 주소 확인 간격을 초 단위로 설정합니다.
    *   `settings.proxied`: Cloudflare 프록시 사용 여부를 설정합니다.

