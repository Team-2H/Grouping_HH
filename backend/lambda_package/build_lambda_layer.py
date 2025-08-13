import shutil
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).parent
PACKAGE_DIR = BASE_DIR / "python"
INSTALL_DIR = BASE_DIR / "python/python"
ZIP_NAME = BASE_DIR / "lambda_layer_package.zip"
REQUIREMENTS_FILE = BASE_DIR / "requirements_lambda.txt"

def clean_package():
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir()

def install_requirements():
    if REQUIREMENTS_FILE.exists():
        subprocess.check_call([
            "pip", "install",
            "-r", str(REQUIREMENTS_FILE),
            "-t", str(INSTALL_DIR)
        ])
    else:
        print("⚠️ requirements.txt not found. Skipping dependency installation.")

def create_zip():
    if ZIP_NAME.exists():
        ZIP_NAME.unlink()
    shutil.make_archive(str(ZIP_NAME.with_suffix("")), "zip", PACKAGE_DIR)
    print(f"📦 Created zip: {ZIP_NAME}")



if __name__ == "__main__":
    clean_package()
    install_requirements()
    create_zip()
    print("🎯 Lambda package build completed!")
