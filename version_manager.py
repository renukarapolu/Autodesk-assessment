import os
import re
import logging
from pathlib import Path

# Setup basic logging for production visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_file_content(file_path, pattern, replacement):
    """
    Reads a file, applies a regex substitution, and writes it back safely.
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return

    try:
        content = file_path.read_text()
        new_content = re.sub(pattern, replacement, content)

        if content == new_content:
            logger.info(f"No version change needed for {file_path.name}.")
            return

        file_path.write_text(new_content)
        # Setting permissions to 755 (standard for build scripts/configs)
        file_path.chmod(0o755)
        logger.info(f"Successfully updated {file_path.name}")

    except Exception as e:
        logger.error(f"Critical error updating {file_path.name}: {e}")

def main():
    # Extracting environment variables
    source_path = os.environ.get("SourcePath")
    build_num = os.environ.get("BuildNum")

    if not all([source_path, build_num]):
        logger.error("Environment variables 'SourcePath' or 'BuildNum' are missing.")
        return

    # Define paths using pathlib for cross-platform reliability
    base_dir = Path(source_path) / "develop" / "global" / "src"

    # Map of files to their respective regex patterns
    # Using capturing groups to keep the identifiers intact
    updates = [
        (base_dir / "SConstruct", r"(point=)\d+", rf"\1{build_num}"),
        (base_dir / "VERSION", r"(ADLMSDK_VERSION_POINT=\s*)\d+", rf"\1{build_num}")
    ]

    for file_path, pattern, replacement in updates:
        update_file_content(file_path, pattern, replacement)

if __name__ == "__main__":
    main()