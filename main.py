import json
import random
from enum import Enum
from datetime import datetime
from typing import List, Dict, Any, Optional


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class QuestionType(Enum):
    MULTIPLE_CHOICE = 1
    TRUE_FALSE = 2
    FILL_BLANK = 3


class FootballQuiz:
    def __init__(self):
        self.questions = self.load_questions()
        self.score = 0
        self.current_question_index = 0
        self.quiz_start_time = None
        self.quiz_end_time = None
        self.asked_questions = []

    def load_questions(self) -> List[Dict[str, Any]]:
        """Load football questions from a data structure"""
        return [
            {
                "id": 1,
                "question": "Which country won the 2018 FIFA World Cup?",
                "type": QuestionType.MULTIPLE_CHOICE,
                "options": ["France", "Croatia", "Belgium", "England"],
                "correct_answer": "France",
                "difficulty": Difficulty.EASY,
                "topic": "World Cup"
            },
            {
                "id": 2,
                "question": "Lionel Messi has never won a World Cup. True or False?",
                "type": QuestionType.TRUE_FALSE,
                "correct_answer": "False",
                "difficulty": Difficulty.EASY,
                "topic": "Players"
            },
            {
                "id": 3,
                "question": "Which club has won the most UEFA Champions League titles?",
                "type": QuestionType.MULTIPLE_CHOICE,
                "options": ["Real Madrid", "AC Milan", "Bayern Munich", "Barcelona"],
                "correct_answer": "Real Madrid",
                "difficulty": Difficulty.MEDIUM,
                "topic": "Clubs"
            },
            {
                "id": 4,
                "question": "The __________ is the trophy awarded to the winners of the UEFA European Championship.",
                "type": QuestionType.FILL_BLANK,
                "correct_answer": "Henri Delaunay Trophy",
                "difficulty": Difficulty.MEDIUM,
                "topic": "Tournaments"
            },
            {
                "id": 5,
                "question": "Which player has scored the most goals in a single Premier League season?",
                "type": QuestionType.MULTIPLE_CHOICE,
                "options": ["Mohamed Salah", "Alan Shearer", "Erling Haaland", "Andy Cole"],
                "correct_answer": "Erling Haaland",
                "difficulty": Difficulty.HARD,
                "topic": "Records"
            },
            {
                "id": 6,
                "question": "Pele scored over 1000 career goals. True or False?",
                "type": QuestionType.TRUE_FALSE,
                "correct_answer": "True",
                "difficulty": Difficulty.MEDIUM,
                "topic": "Players"
            },
            {
                "id": 7,
                "question": "The 2022 World Cup was held in __________.",
                "type": QuestionType.FILL_BLANK,
                "correct_answer": "Qatar",
                "difficulty": Difficulty.EASY,
                "topic": "World Cup"
            },
            {
                "id": 8,
                "question": "Which country has won the most Copa América titles?",
                "type": QuestionType.MULTIPLE_CHOICE,
                "options": ["Brazil", "Argentina", "Uruguay", "Chile"],
                "correct_answer": "Uruguay",
                "difficulty": Difficulty.HARD,
                "topic": "Tournaments"
            },
            {
                "id": 9,
                "question": "Diego Maradona's 'Hand of God' goal was against England. True or False?",
                "type": QuestionType.TRUE_FALSE,
                "correct_answer": "True",
                "difficulty": Difficulty.EASY,
                "topic": "History"
            },
            {
                "id": 10,
                "question": "The __________ is awarded to the best player at the FIFA World Cup.",
                "type": QuestionType.FILL_BLANK,
                "correct_answer": "Golden Ball",
                "difficulty": Difficulty.MEDIUM,
                "topic": "Awards"
            }
        ]

    def start_quiz(self, num_questions: int = 5, topics: Optional[List[str]] = None,
                   difficulty: Optional[Difficulty] = None) -> Dict[str, Any]:
        """Start a new quiz with optional filters"""
        self.score = 0
        self.current_question_index = 0
        self.quiz_start_time = datetime.now()
        self.asked_questions = []

        # Filter questions based on parameters
        filtered_questions = self.questions
        if topics:
            filtered_questions = [q for q in filtered_questions if q["topic"] in topics]
        if difficulty:
            filtered_questions = [q for q in filtered_questions if q["difficulty"] == difficulty]

        # Select random questions
        num_questions = min(num_questions, len(filtered_questions))
        self.asked_questions = random.sample(filtered_questions, num_questions)

        return {
            "status": "started",
            "total_questions": num_questions,
            "topics": topics if topics else "All",
            "difficulty": difficulty.name if difficulty else "Mixed"
        }

    def get_next_question(self) -> Optional[Dict[str, Any]]:
        """Get the next question in the quiz"""
        if self.current_question_index >= len(self.asked_questions):
            return None

        question = self.asked_questions[self.current_question_index]
        # Remove the correct answer from the returned question
        question_display = question.copy()
        if "correct_answer" in question_display:
            del question_display["correct_answer"]

        return question_display

    def submit_answer(self, answer: str) -> Dict[str, Any]:
        """Submit an answer for the current question"""
        if self.current_question_index >= len(self.asked_questions):
            return {"error": "No more questions in the quiz"}

        current_question = self.asked_questions[self.current_question_index]
        is_correct = False

        # Check answer based on question type
        if current_question["type"] == QuestionType.TRUE_FALSE:
            is_correct = answer.lower() == current_question["correct_answer"].lower()
        elif current_question["type"] == QuestionType.MULTIPLE_CHOICE:
            is_correct = answer.lower() == current_question["correct_answer"].lower()
        elif current_question["type"] == QuestionType.FILL_BLANK:
            # For fill in the blank, we'll do a case-insensitive partial match
            is_correct = current_question["correct_answer"].lower() in answer.lower()

        if is_correct:
            self.score += 1

        self.current_question_index += 1

        # Check if quiz is complete
        quiz_complete = self.current_question_index >= len(self.asked_questions)
        if quiz_complete:
            self.quiz_end_time = datetime.now()

        return {
            "is_correct": is_correct,
            "correct_answer": current_question["correct_answer"],
            "current_score": self.score,
            "question_number": self.current_question_index,
            "total_questions": len(self.asked_questions),
            "quiz_complete": quiz_complete
        }

    def get_quiz_results(self) -> Dict[str, Any]:
        """Get the final results of the quiz"""
        if not self.quiz_end_time:
            return {"error": "Quiz is not yet complete"}

        time_taken = (self.quiz_end_time - self.quiz_start_time).total_seconds()

        return {
            "final_score": self.score,
            "total_questions": len(self.asked_questions),
            "percentage": (self.score / len(self.asked_questions)) * 100,
            "time_taken_seconds": round(time_taken, 2),
            "performance": self._get_performance_rating()
        }

    def _get_performance_rating(self) -> str:
        """Get a performance rating based on the score"""
        percentage = (self.score / len(self.asked_questions)) * 100

        if percentage >= 90:
            return "World Class!"
        elif percentage >= 75:
            return "Professional Level"
        elif percentage >= 60:
            return "First Division"
        elif percentage >= 40:
            return "Semi-Pro"
        else:
            return "Sunday League"

    def get_question_statistics(self) -> Dict[str, Any]:
        """Get statistics about available questions"""
        topics = {}
        difficulties = {}

        for question in self.questions:
            # Count questions by topic
            topic = question["topic"]
            topics[topic] = topics.get(topic, 0) + 1

            # Count questions by difficulty
            difficulty = question["difficulty"].name
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1

        return {
            "total_questions": len(self.questions),
            "topics": topics,
            "difficulties": difficulties
        }


# Example usage and demonstration
def demonstrate_quiz():
    """Demonstrate the football quiz functionality"""
    quiz = FootballQuiz()

    # Display available questions statistics
    stats = quiz.get_question_statistics()
    print("Football Quiz - Question Statistics")
    print(f"Total questions: {stats['total_questions']}")
    print("Topics:", json.dumps(stats['topics'], indent=2))
    print("Difficulties:", json.dumps(stats['difficulties'], indent=2))
    print()

    # Start a quiz with 3 questions
    print("Starting a new quiz with 3 questions...")
    quiz.start_quiz(num_questions=3)

    # Answer questions
    question_count = 1
    while True:
        question = quiz.get_next_question()
        if not question:
            break

        print(f"Question {question_count}: {question['question']}")

        # Handle different question types
        if question["type"] == QuestionType.MULTIPLE_CHOICE:
            for i, option in enumerate(question["options"], 1):
                print(f"  {i}. {option}")
            answer = input("Your answer (enter option number or text): ")
            # Simple input handling - in a real app, you'd validate this
            if answer.isdigit() and 1 <= int(answer) <= len(question["options"]):
                answer = question["options"][int(answer) - 1]
        elif question["type"] == QuestionType.TRUE_FALSE:
            answer = input("Your answer (True/False): ")
        elif question["type"] == QuestionType.FILL_BLANK:
            answer = input("Fill in the blank: ")

        result = quiz.submit_answer(answer)
        if result["is_correct"]:
            print("✅ Correct!")
        else:
            print(f"❌ Wrong! The correct answer was: {result['correct_answer']}")

        print(f"Current score: {result['current_score']}/{result['total_questions']}")
        print()
        question_count += 1

    # Show final results
    results = quiz.get_quiz_results()
    print("Quiz Complete!")
    print(f"Final Score: {results['final_score']}/{results['total_questions']}")
    print(f"Percentage: {results['percentage']:.1f}%")
    print(f"Time taken: {results['time_taken_seconds']} seconds")
    print(f"Performance: {results['performance']}")


# For use as a backend module
if __name__ == "__main__":
    demonstrate_quiz()