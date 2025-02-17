import time
import requests
import yaml
from typing import Dict, Any

class ConfigLoader:
    def __init__(self, config_path: str = 'config.yml'):
        self.config = self._load_config(config_path)
        
    def _load_config(self, path: str) -> Dict[str, Any]:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
        
    @property
    def cloudflare(self) -> Dict[str, Any]:
        return self.config['cloudflare']
    
    @property
    def ip_api_url(self) -> str:
        return self.config['ip_check']['api_url']
    
    @property
    def interval(self) -> int:
        return self.config['settings']['interval']
    
    @property
    def proxied(self) -> bool:
        return self.config['settings']['proxied']

class CloudflareDDNSUpdater:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {self.config.cloudflare['api_token']}",
            "Content-Type": "application/json"
        }

    def get_current_ip(self) -> str:
        """
        외부 IP를 조회합니다.
        """
        try:
            res = requests.get(self.config.ip_api_url)
            if res.status_code == 200:
                return res.text.strip()
            else:
                print("IP 조회 실패:", res.status_code)
                return None
        except Exception as e:
            print("IP 조회 중 오류 발생:", e)
            return None

    def get_dns_record_id(self) -> str:
        """
        DNS A 레코드의 record ID를 Cloudflare API를 통해 조회합니다.
        """
        url = f"https://api.cloudflare.com/client/v4/zones/{self.config.cloudflare['zone_id']}/dns_records?type=A&name={self.config.cloudflare['record_name']}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data["result"]:
                return data["result"][0]["id"]
            else:
                return None
        else:
            print("DNS 레코드 조회 실패:", response.status_code)
            return None

    def update_dns_record(self, record_id: str, ip: str) -> Dict[str, Any]:
        """
        기존 A 레코드를 업데이트합니다.
        """
        url = f"https://api.cloudflare.com/client/v4/zones/{self.config.cloudflare['zone_id']}/dns_records/{record_id}"
        payload = {
            "type": "A",
            "name": self.config.cloudflare['record_name'],
            "content": ip,
            "ttl": 1,
            "proxied": self.config.proxied
        }
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def create_dns_record(self, ip: str) -> Dict[str, Any]:
        """
        새로운 A 레코드를 생성합니다.
        """
        url = f"https://api.cloudflare.com/client/v4/zones/{self.config.cloudflare['zone_id']}/dns_records"
        payload = {
            "type": "A",
            "name": self.config.cloudflare['record_name'],
            "content": ip,
            "ttl": 1,
            "proxied": self.config.proxied
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def run(self):
        record_id = self.get_dns_record_id()
        if record_id:
            print("기존 DNS 레코드 발견. Record ID:", record_id)
        else:
            print("기존 DNS 레코드가 없습니다. 새로운 레코드를 생성합니다.")

        while True:
            ip = self.get_current_ip()
            if ip:
                print("현재 공인 IP:", ip)
                if record_id:
                    result = self.update_dns_record(record_id, ip)
                    if result.get("success"):
                        print("DNS 레코드 업데이트 성공:", result)
                    else:
                        print("DNS 레코드 업데이트 실패:", result)
                else:
                    result = self.create_dns_record(ip)
                    if result.get("success"):
                        print("DNS 레코드 생성 성공:", result)
                        record_id = result["result"]["id"]
                    else:
                        print("DNS 레코드 생성 실패:", result)
            else:
                print("IP를 가져오지 못했습니다.")

            time.sleep(self.config.interval)

if __name__ == "__main__":
    config = ConfigLoader()
    updater = CloudflareDDNSUpdater(config)
    updater.run()
