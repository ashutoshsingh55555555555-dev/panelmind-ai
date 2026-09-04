
# utils/questions.py

# Base interview questions
TECHNICAL_QUESTIONS = [
    "Tell me about a technical project you have worked on.",
    "Why did you choose the technologies used in your project?",
    "How did you handle errors or unexpected problems in your project?",
    "How would you improve the performance of your application?",
    "Explain one technical concept that you are confident about.",
    "How do you design an API that is reliable, secure, and easy to maintain?",
    "How do you approach testing a feature before releasing it to users?",
    "Describe a time you had to debug a difficult production issue.",
    "How would you design a system to handle a sudden increase in traffic?",
    "What trade-offs do you consider when choosing between two technical approaches?"
]

HR_QUESTIONS = [
    "Tell me about yourself.",
    "What is your biggest strength?",
    "Tell me about a challenge you faced and how you solved it.",
    "Why should we hire you?",
    "Where do you see yourself in the next five years?",
    "Tell me about a time you received difficult feedback.",
    "Describe a situation where you had to work with a difficult teammate.",
    "How do you prioritize when you have several urgent tasks?",
    "Tell me about a mistake you made and what you learned from it.",
    "What kind of work environment helps you perform at your best?"
]

GENERAL_QUESTIONS = [
    "Tell me about yourself.",
    "What is your biggest achievement?",
    "Describe a difficult problem you solved.",
    "How do you handle pressure?",
    "Why do you want to join our organization?",
    "Tell me about a time you showed leadership.",
    "How do you learn a new skill or technology?",
    "Describe a time you had to adapt to a major change.",
    "What motivates you to do your best work?",
    "What questions would you ask an interviewer at the end of a round?"
]


def get_questions(interview_type, num_questions=5):
    """
    Return base interview questions according to interview type.
    """

    if interview_type == "Technical Interview":
        questions = TECHNICAL_QUESTIONS

    elif interview_type == "HR Interview":
        questions = HR_QUESTIONS

    else:
        questions = GENERAL_QUESTIONS

    return questions[:num_questions]


def get_follow_up_question(answer, difficulty="medium", question=""):
    """
    Generate an adaptive follow-up question based on the candidate's answer.

    difficulty:
        weak       -> clarifying question
        medium     -> deeper question
        strong     -> challenging question
    """

    answer = answer.strip()
    answer_lower = answer.lower()
    question_lower = question.lower()

    if "react" in answer_lower or "frontend" in answer_lower:
        focus_prompt = (
            "Why did you choose that frontend approach over a simpler option, "
            "and how did you manage state across components?"
        )
    elif any(word in answer_lower for word in ("database", "sql", "query")):
        focus_prompt = (
            "How did you choose the data model, and what did you do to keep "
            "queries reliable and efficient as usage grew?"
        )
    elif any(word in answer_lower for word in ("team", "collaborated", "stakeholder")):
        focus_prompt = (
            "What was your specific contribution, and how did you handle a "
            "different opinion from a teammate or stakeholder?"
        )
    elif any(word in answer_lower for word in ("challenge", "problem", "issue", "bug")):
        focus_prompt = (
            "How did you isolate the root cause, and what measurable result "
            "did your solution produce?"
        )
    elif "why" in question_lower or "choose" in question_lower:
        focus_prompt = (
            "What evidence guided that decision, and what trade-off did you "
            "accept by choosing it?"
        )
    else:
        focus_prompt = (
            "What was your exact contribution, and what measurable result "
            "did you achieve?"
        )

    # Empty or extremely short answer
    if len(answer) < 30:

        return (
            "Can you explain your answer in more detail and "
            "give a specific example from your experience?"
        )

    # Strong answer
    if difficulty == "strong":

        return (
            "That's interesting. Now let's go deeper: " + focus_prompt
        )

    # Weak answer
    elif difficulty == "weak":

        return (
            "Can you clarify that? What exactly did you do, "
            "and what was the result?"
        )

    # Medium answer
    else:

        return (
            "Can you explain that with one specific example? " + focus_prompt
        )


def calculate_answer_strength(answer):
    """
    Simple rule-based answer strength detector.

    Returns:
        weak / medium / strong
    """

    answer = answer.strip()

    words = answer.split()
    word_count = len(words)

    # Weak answer
    if word_count < 10:
        return "weak"

    # Look for evidence of a detailed answer
    strong_keywords = [
        "because",
        "implemented",
        "developed",
        "solved",
        "result",
        "improved",
        "example",
        "project",
        "experience",
        "challenge",
        "performance",
        "testing"
    ]

    keyword_count = sum(
        1 for word in strong_keywords
        if word.lower() in answer.lower()
    )

    if word_count >= 50 and keyword_count >= 3:
        return "strong"

    return "medium"


def get_adaptive_follow_up(answer, question=""):
    """
    Analyze the candidate's answer and return:
    1. answer strength
    2. adaptive follow-up question
    """

    strength = calculate_answer_strength(answer)

    follow_up = get_follow_up_question(
        answer,
        strength,
        question
    )

    return {
        "strength": strength,
        "follow_up": follow_up
    }
