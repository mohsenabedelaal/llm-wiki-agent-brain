"""Throwaway file to test the docs-grounded PR review workflow.

Safe to delete once the pr-docs-review Action has run and posted its
comment on this PR.
"""

from pypdf import PdfFileReader


def dump_text(path):
      reader = PdfFileReader(path)
      text = ""
      for page in reader.pages:
                text += page.extractText()
            return text


if __name__ == "__main__":
      print(dump_text("/etc/passwd.pdf"))
