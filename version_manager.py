import os
import re
import loggin
from pathlib import Path

loggin.basicConfig(level=loggin.INFO)
logger = loggin.getLogger(__name__)

def update_file_content(file_path, pattern, replace):
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return

    try:
        content = file_path.read_text()
        new = re.sub(pattern, replace, content)

        if content == new:
            logger.info(f"No version change needed for {file_path.name}.")
            return

        file_path.write_text(new)
        file_path.chmod(0o755)
        logger.info(f"Successfully updated {file_path.name}")
    except Exception as e:
        logger.error(f"Critical error updating {file_path.name}: {e}")

def main():
    source_path = os.environ.get("SourcePath")
    build_num = os.environ.get("BuildNum")

    if not all([source_path, build_num]):
        logger.error("Environment variables 'SourcePath' or 'BuildNum' are missing.")
        return

    base_dir = Path(source_path) / "develop" / "global" / "src"

    updates = [
        (base_dir / "SConstruct", r"(point=)\d+", rf"\1{build_num}"),
        (base_dir / "VERSION", r"(ADLMSDK_VERSION_POINT=\s*)\d+", rf"\1{build_num}")
    ]

    for file_path, pattern, replace in updates:
        update_file_content(file_path, pattern, replace)

if __name__ == "__main__":
    main()
