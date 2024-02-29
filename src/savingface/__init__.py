"""Import all the patching functions and run 'em if you got 'em."""

from .patch import patch_from_pretrained, patch_repository_push


def save_face():
    """Monkey patch the functions to save face."""
    patch_repository_push()
    patch_from_pretrained()


def is_installed() -> bool:
    """Placeholder to check if installed :)"""
    return True
