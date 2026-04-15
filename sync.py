import urllib.parse
import requests

USER_EMAIL = "seokwangwon@hotmail.com"

# 1. 맨 끝의 슬래시(/)를 제거한 경로
FOLDER_PATH = "Apps/remotely-save/MyVault/2. AREA/Report - Industry"

# 2. 경로에 포함된 띄어쓰기나 특수기호를 웹 주소용으로 안전하게 변환 (URL 인코딩)
encoded_path = urllib.parse.quote(FOLDER_PATH)

# 3. 최종 API 호출 주소 생성
endpoint = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{encoded_path}:/children"

# (참고) 이후 토큰을 헤더에 담아 호출하는 부분
# headers = {"Authorization": f"Bearer {access_token}"}
# response = requests.get(endpoint, headers=headers)
