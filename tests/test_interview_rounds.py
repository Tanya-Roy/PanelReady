import os
import tempfile
import unittest
from pathlib import Path

_test_data = tempfile.TemporaryDirectory()
os.environ["DATABASE_PATH"] = str(Path(_test_data.name) / "interviews.sqlite3")

from app import (
    INTERVIEW_QUESTION_CATEGORIES,
    INTERVIEW_ROUNDS,
    annotate_interview_rounds,
    assign_interview_rounds,
    question_round_progress,
)


class InterviewRoundTests(unittest.TestCase):
    def setUp(self):
        self.plan = assign_interview_rounds(
            [
                {
                    "category": category,
                    "topic": category,
                    "project": "",
                    "question": f"Question about {category}?",
                }
                for category in INTERVIEW_QUESTION_CATEGORIES
            ]
        )

    def test_plan_groups_ten_questions_into_three_rounds(self):
        self.assertEqual(len(self.plan), 10)
        self.assertEqual(
            [question["round_number"] for question in self.plan],
            [1] * 4 + [2] * 3 + [3] * 3,
        )
        self.assertEqual(
            {question["interviewer"] for question in self.plan[:4]},
            {"Technical lead"},
        )
        self.assertEqual(
            {question["interviewer"] for question in self.plan[4:7]},
            {"HR interviewer"},
        )
        self.assertEqual(
            {question["interviewer"] for question in self.plan[7:]},
            {"Hiring manager"},
        )

    def test_round_progress_reports_question_position(self):
        progress = question_round_progress(self.plan, 4)

        self.assertEqual(
            progress,
            {
                "number": 2,
                "name": "Behavioral interview",
                "interviewer": "HR interviewer",
                "question_number": 1,
                "question_count": 3,
            },
        )

    def test_transcript_answers_keep_the_interviewer_for_their_round(self):
        transcript = [
            {"speaker": "interviewer", "plan_index": 0},
            {"speaker": "candidate", "text": "Technical answer"},
            {"speaker": "interviewer", "plan_index": 4},
            {"speaker": "candidate", "text": "Behavioral answer"},
        ]

        annotate_interview_rounds(transcript, self.plan)

        self.assertEqual(transcript[1]["interviewer"], "Technical lead")
        self.assertEqual(transcript[3]["interviewer"], "HR interviewer")
        self.assertEqual([item["number"] for item in INTERVIEW_ROUNDS], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
