from enum import Enum


class QualityMetric(str, Enum):
    CI_CD = "ci_cd"
    DOCUMENTATION = "documentation"
    LICENSE = "license"
    OPEN_ISSUES = "open_issues"
    README = "readme"
    RECENT_ACTIVITY = "recent_activity"
    TEST_COVERAGE = "test_coverage"

    def __str__(self) -> str:
        return str(self.value)
