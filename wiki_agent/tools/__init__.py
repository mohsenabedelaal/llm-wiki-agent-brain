"""Vault filesystem tools for the LLM Wiki agent."""

from .vault import (
    append_log,
    list_vault,
    read_file,
    read_index,
    read_pdf,
    update_hot,
    write_file,
)

__all__ = [
    "append_log",
    "list_vault",
    "read_file",
    "read_index",
    "read_pdf",
    "update_hot",
    "write_file",
]
