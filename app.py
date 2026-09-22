"""Vercel ASGI entrypoint at repo root (required by Vercel module path resolution)."""

from sentryeval.app import app

__all__ = ["app"]
