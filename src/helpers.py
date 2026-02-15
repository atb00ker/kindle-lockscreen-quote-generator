from pathlib import Path


def find_project_root(start_path=None):
    """
    Find the project root by locating pyproject.toml.

    Args:
        start_path: Starting directory for search (defaults to this file's directory)

    Returns:
        Path object pointing to project root, or None if not found
    """
    if start_path is None:
        start_path = Path(__file__).resolve().parent
    else:
        start_path = Path(start_path).resolve()

    current = start_path
    # Walk up the directory tree
    for parent in [current] + list(current.parents):
        pyproject_path = parent / "pyproject.toml"
        if pyproject_path.exists():
            return parent

    return None
