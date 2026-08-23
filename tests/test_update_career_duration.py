import datetime as dt
import unittest

from scripts.update_career_duration import calculate_duration, update_readme


class CalculateDurationTest(unittest.TestCase):
    def test_calculates_completed_years_and_months(self) -> None:
        self.assertEqual(calculate_duration(2022, 7, dt.date(2026, 8, 23)), "4년 1개월")

    def test_omits_zero_months(self) -> None:
        self.assertEqual(calculate_duration(2022, 7, dt.date(2026, 7, 1)), "4년")

    def test_rejects_a_date_before_the_start_month(self) -> None:
        with self.assertRaises(ValueError):
            calculate_duration(2022, 7, dt.date(2022, 6, 30))


class UpdateReadmeTest(unittest.TestCase):
    def test_replaces_only_the_career_duration_marker(self) -> None:
        source = (
            "소개\n"
            "<!-- career-duration:start -->기존 값<!-- career-duration:end -->\n"
            "나머지 내용\n"
        )

        updated = update_readme(source, "4년 1개월")

        self.assertEqual(
            updated,
            "소개\n"
            "<!-- career-duration:start -->4년 1개월<!-- career-duration:end -->\n"
            "나머지 내용\n",
        )

    def test_requires_exactly_one_marker_pair(self) -> None:
        with self.assertRaises(ValueError):
            update_readme("표시 구간 없음", "4년")


if __name__ == "__main__":
    unittest.main()
