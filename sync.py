# sync.py의 핵심 API 호출 예시 (MSAL 라이브러리 사용)
# Application Permission을 사용할 때는 /users/{사용자 계정} 경로를 사용해야 해.

USER_EMAIL = "너의_마이크로소프트_계정@도메인.com"
FOLDER_PATH = "Notes" # 동기화할 OneDrive 폴더 이름

# MS Graph API 엔드포인트
endpoint = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{FOLDER_PATH}:/children"

# 이후 부여받은 토큰(access_token)을 헤더에 담아 위 endpoint로 요청을 보내어 파일을 다운로드하는 로직 작성
