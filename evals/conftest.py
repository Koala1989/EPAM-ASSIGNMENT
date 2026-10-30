"""Prints the retrieval eval's Hit@k and MRR summary at the end of a pytest run that included it."""

import sys


def pytest_terminal_summary(terminalreporter):
    test_retrieval = sys.modules.get("test_retrieval")
    if test_retrieval is None:  # the run did not include the retrieval eval
        return
    summary = test_retrieval.pytest_terminal_summary_mrr()
    if summary:
        terminalreporter.section("retrieval ranking")
        terminalreporter.write_line(summary)
