#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows EXE 빌드 스크립트
Usage: python build_exe.py
"""
import os
import sys
import subprocess

def build_exe():
    """PyInstaller를 사용하여 Windows EXE 생성"""
    
    app_path = os.path.abspath("hr_app.py")
    output_dir = os.path.abspath("dist")
    
    print("=" * 60)
    print("SEOJIN HR & ATTENDANCE - Windows EXE 빌드")
    print("=" * 60)
    
    # PyInstaller 명령어
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",                          # 단일 EXE 파일로 생성
        "--windowed",                         # 콘솔 창 없음
        "--name=hr_app",                     # 실행 파일명
        "--icon=hr_app.ico" if os.path.exists("hr_app.ico") else "",  # 아이콘
        f"--distpath={output_dir}",           # 출력 디렉토리
        "--add-data=.:.",                     # 현재 디렉토리 포함
        app_path
    ]
    
    # 빈 인자 제거
    cmd = [arg for arg in cmd if arg]
    
    print("\n빌드 명령어:")
    print(" ".join(cmd))
    print("\n빌드 시작 (시간이 걸릴 수 있습니다)...")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, cwd=os.path.dirname(app_path))
        
        exe_path = os.path.join(output_dir, "hr_app.exe")
        if os.path.exists(exe_path):
            print("\n" + "=" * 60)
            print("✓ 빌드 성공!")
            print(f"  생성된 EXE: {exe_path}")
            print(f"  파일 크기: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
            print("=" * 60)
            return True
        else:
            print("\n✗ 오류: EXE 파일이 생성되지 않았습니다.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 빌드 실패: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 오류: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
