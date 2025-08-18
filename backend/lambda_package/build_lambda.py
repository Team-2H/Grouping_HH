import shutil
from pathlib import Path
import docker
import os


BASE_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).resolve().parent.parent
PACKAGE_DIR = BASE_DIR / "package"
FILE_LIST_FILE = BASE_DIR / "file_list.txt"

# 패키징 할 폴더 하위 삭제
def clean_package():
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir()

# file_list.txt에 적힌 파일들만 복사해서 패키징할 폴더 하위로 복사
def copy_files():
    if not FILE_LIST_FILE.exists():
        print("⚠️ file_list.txt not found. Skipping file copy.")
        return

    with open(FILE_LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            src = (PROJECT_DIR / line.strip()).resolve()
            if src.exists():
                target_path = PACKAGE_DIR / Path(line.strip())
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target_path)
                print(f"✅ Copied: {src} -> {target_path}")
            else:
                print(f"⚠️ File not found: {src}")

# docker 이미지 생성
def package_docker_image():
    client = docker.from_env()

    # 이미지 빌드 (Dockerfile은 현재 디렉토리 기준)
    image, logs = client.images.build(path=str(BASE_DIR), tag="groupingproject:latest")

    # 로그 출력
    for chunk in logs:
        if isinstance(chunk, dict):
            stream_msg = chunk.get("stream")
            if stream_msg and isinstance(stream_msg, str):
                print(stream_msg.strip())

    print("이미지 빌드 완료:", image.tags)

# 패키징 폴더 삭제
def deletePackageFolder():
    if os.path.exists(PACKAGE_DIR) and os.path.isdir(PACKAGE_DIR):
        shutil.rmtree(PACKAGE_DIR)
        print(f"{PACKAGE_DIR} 폴더를 삭제했습니다.")
    else:
        print(f"{PACKAGE_DIR} 폴더가 존재하지 않거나 디렉터리가 아닙니다.")


if __name__ == "__main__":
    clean_package()
    copy_files()
    package_docker_image()
    deletePackageFolder()
    print("🎯 Lambda package build completed!")

