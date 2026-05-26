# GitHub 배포 가이드

SEOJIN HR & ATTENDANCE를 GitHub에 배포하는 방법을 설명합니다.

## 📋 필수 사항

- GitHub 계정 (없으면 [github.com](https://github.com)에서 가입)
- Git 설치 ([git-scm.com](https://git-scm.com))

## 🚀 배포 단계

### Step 1: GitHub 저장소 생성

1. [GitHub](https://github.com)에 로그인
2. 우측 상단 `+` 버튼 → **New repository**
3. 저장소 이름: `hr-attendance`
4. 설명: `인사/근태 관리 시스템 - HR & Attendance Management`
5. **Public** 선택 (공개)
6. **Create repository** 클릭

### Step 2: 로컬 저장소와 GitHub 연결

터미널/명령 프롬프트에서:

```bash
cd /path/to/hr-attendance

# 원격 저장소 추가
git remote add origin https://github.com/your-username/hr-attendance.git

# 또는 SSH 사용 (설정된 경우)
git remote add origin git@github.com:your-username/hr-attendance.git

# 브랜치명 변경 (필요시)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

**주의**: `your-username`을 실제 GitHub 사용자명으로 변경하세요.

### Step 3: 태그(버전) 생성

릴리스를 생성하기 위해 태그를 만듭니다:

```bash
# 태그 생성
git tag -a v1.0.0 -m "Release version 1.0.0"

# GitHub에 태그 푸시
git push origin v1.0.0
```

또는 모든 태그 한 번에:

```bash
git push origin --tags
```

### Step 4: GitHub Release 생성

1. GitHub 저장소 페이지 → **Releases**
2. **Create a new release** 클릭
3. 태그: `v1.0.0` 선택
4. 제목: `SEOJIN HR v1.0.0`
5. 설명:
```markdown
# SEOJIN HR & ATTENDANCE v1.0.0

## 주요 기능
- 직원 정보 관리
- 출퇴근 기록 및 자동 시간 계산
- 휴가 신청 및 승인
- 월별 급여 자동 계산
- 근무 통계 및 분석

## 설치 방법
1. `hr_app.exe` 다운로드
2. 실행하면 됩니다

## 사용자 매뉴얼
[SEOJIN_HR_사용자매뉴얼.pdf](SEOJIN_HR_사용자매뉴얼.pdf) 참고

## 시스템 요구사항
- Windows 7 이상 또는 macOS 10.13 이상
- RAM: 2GB 이상
- 디스크: 100MB 이상
```

6. **Publish release** 클릭

### Step 5: 자동 빌드 확인

GitHub Actions를 통해 자동으로 Windows EXE가 빌드됩니다:

1. 저장소 → **Actions** 탭
2. **Build Windows EXE** 워크플로우 확인
3. 빌드 완료 후 **Releases**에서 EXE 파일 다운로드 가능

## 📝 이후 업데이트

새 버전을 배포할 때:

```bash
# 코드 수정 후
git add .
git commit -m "v1.1.0: 새로운 기능 추가"

# 버전 태그
git tag -a v1.1.0 -m "Release version 1.1.0"

# GitHub에 푸시
git push origin main
git push origin v1.1.0
```

GitHub에서 자동으로 새 EXE를 빌드하고 Release를 생성할 수 있습니다.

## 🔒 보안 팁

### SSH 키 설정 (선택사항)

더 안전한 연결을 위해 SSH 키를 설정할 수 있습니다:

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your-email@example.com"

# GitHub 계정에 공개 키 추가
# Settings → SSH and GPG keys → New SSH key
```

### 민감한 정보 보호

**.gitignore** 확인:
- `hr.db` (데이터베이스) - 포함되지 않음 ✓
- 설정 파일 - 필요시 제외
- 로그 파일 - 포함되지 않음 ✓

## 📚 추가 자료

- [GitHub 가이드](https://docs.github.com/)
- [Git 튜토리얼](https://git-scm.com/book/ko/v2)
- [GitHub Actions 문서](https://docs.github.com/en/actions)

---

**문의**: 배포 중 문제가 발생하면 GitHub Issues에서 도움을 요청하세요.
