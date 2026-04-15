import os
import requests
import msal
import urllib.parse

# 1. 전하께서 하명하신 기본 설정 정보
USER_EMAIL = "seokwangwon@hotmail.com"
ONEDRIVE_PATH = "Apps/remotely-save/MyVault/2. AREA/Report - Industry"
TARGET_DIR = "content"  # Quartz가 인식하는 콘텐츠 폴더

# 2. GitHub Secrets에서 환경 변수 읽기
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
TENANT_ID = os.environ.get("AZURE_TENANT_ID")

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    # 앱 권한(Application Permission)을 위한 토큰 요청
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"토큰 발급 실패: {result.get('error_description')}")

def sync_onedrive_to_github():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 경로 인코딩 및 엔드포인트 설정
    encoded_path = urllib.parse.quote(ONEDRIVE_PATH)
    endpoint = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{encoded_path}:/children"
    
    # 1. 대상 폴더 생성
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Directory {TARGET_DIR} created.")

    # 2. OneDrive 파일 목록 가져오기
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching files: {response.text}")
        return

    items = response.json().get("value", [])
    
    for item in items:
        file_name = item["name"]
        # 파일만 다운로드 (폴더 제외 - 필요 시 재귀 로직 추가 가능)
        if "file" in item:
            download_url = item["@microsoft.graph.downloadUrl"]
            file_content = requests.get(download_url).content
            
            file_path = os.path.join(TARGET_DIR, file_name)
            with open(file_path, "wb") as f:
                f.write(file_content)
            print(f"Downloaded: {file_name}")

if __name__ == "__main__":
    try:
        sync_onedrive_to_github()
        print("✅ OneDrive와 GitHub 간 동기화가 무사히 완료되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
