@echo off
REM SEOJIN HR & ATTENDANCE - Windows EXE 빌드 스크립트
REM Windows 사용자가 쉽게 EXE를 빌드할 수 있도록 제공

echo.
echo ============================================================
echo   SEOJIN HR - Windows EXE 빌드 스크립트
echo ============================================================
echo.

REM Python 설치 확인
python --version >/dev/null 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되지 않았거나 경로에 추가되지 않았습니다.
    echo.
    echo 해결 방법:
    echo 1. Python을 설치하세요 (python.org)
    echo 2. 설치 시 "Add Python to PATH" 체크박스를 선택하세요
    echo 3. 컴퓨터를 재부팅하세요
    echo.
    pause
    exit /b 1
)

echo [정보] Python 버전 확인 중...
python --version

REM PyInstaller 설치 확인
pip show pyinstaller >/dev/null 2>&1
if errorlevel 1 (
    echo.
    echo [정보] PyInstaller 설치 중...
    pip install pyinstaller
    if errorlevel 1 (
        echo [오류] PyInstaller 설치에 실패했습니다.
        pause
        exit /b 1
    )
)

echo.
echo [정보] EXE 빌드 시작...
echo 시간이 걸릴 수 있습니다 (3-5분 소요)
echo.

python build_exe.py

if errorlevel 1 (
    echo.
    echo [오류] 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [성공] EXE 빌드 완료!
echo.
echo 생성된 파일: dist\hr_app.exe
echo.
echo 실행 방법:
echo  1. dist 폴더를 열고 hr_app.exe를 실행하세요
echo  2. 또는 여기서 hr_app.exe로 바로가기를 만드세요
echo ============================================================
echo.

pause
