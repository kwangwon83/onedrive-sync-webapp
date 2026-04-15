import os
import requests
import msal
import urllib.parse

# 1. 전하의 정보 및 경로 설정
USER_EMAIL = "seokwangwon@hotmail.com"
ONEDRIVE_PATH = "Apps/remotely-save/MyVault/2. AREA/Report - Industry"
TARGET_DIR = "content"  # 쿼츠가 지식을 읽어가는 입구이옵니다.

# 2. GitHub Secrets에서 환경 변수 호출
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
TENANT_ID = os.environ.get("AZURE_TENANT_ID")

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    # 앱 권한(Application Permission) 전용 토큰 요청
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"토큰 발급 실패: {result.get('error_description')}")

def sync_onedrive_to_github():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 띄어쓰기 등 특수문자 안전 처리
    encoded_path = urllib.parse.quote(ONEDRIVE_PATH)
    endpoint = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{encoded_path}:/children"
    
    # 지식을 담을 content 폴더가 없다면 생성하옵니다.
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # OneDrive에서 파일 목록 징발
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        raise Exception(f"OneDrive 접근 실패: {response.text}")

    items = response.json().get("value", [])
    
    for item in items:
        file_name = item["name"]
        # 폴더가 아닌 파일인 경우에만 가져오옵니다.
        if "file" in item:
            download_url = item["@microsoft.graph.downloadUrl"]
            file_content = requests.get(download_url).content
            
            # content 폴더 내에 파일 저장
            file_path = os.path.join(TARGET_DIR, file_name)
            with open(file_path, "wb") as f:
                f.write(file_content)
            print(f"징발 완료: {file_name}")

if __name__ == "__main__":
    try:
        sync_onedrive_to_github()
        print("✅ OneDrive의 지식을 content 폴더로 모두 옮겼사옵니다.")
    except Exception as e:
        print(f"❌ 오류가 발생하였나이다: {e}")
        exit(1)
