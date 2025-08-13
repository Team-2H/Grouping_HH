import shutil
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).resolve().parent.parent
PACKAGE_DIR = BASE_DIR / "package"
ZIP_NAME = BASE_DIR / "lambda_package.zip"
FILE_LIST_FILE = BASE_DIR / "file_list.txt"

def clean_package():
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir()

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

def create_zip():
    if ZIP_NAME.exists():
        ZIP_NAME.unlink()
    shutil.make_archive(str(ZIP_NAME.with_suffix("")), "zip", PACKAGE_DIR)
    print(f"📦 Created zip: {ZIP_NAME}")

if __name__ == "__main__":
    clean_package()
    copy_files()
    create_zip()
    print("🎯 Lambda package build completed!")
