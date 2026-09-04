
# utils/analyzer.py


def analyze_answer(question, answer):
    """
    Analyze a candidate's answer.

    Returns a dictionary containing:
    - score
    - strength
    - strengths
    - weaknesses
    - analysis
    """

    answer = answer.strip()

    if not answer:
        return {
            "score": 0,
            "strength": "weak",
            "strengths": ["No answer provided"],
            "weaknesses": ["Candidate did not provide an answer"],
            "analysis": "No answer was provided."
        }

    words = answer.split()
    word_count = len(words)

    # -----------------------------------------
    # Important interview keywords
    # -----------------------------------------
    useful_keywords = [
        "because",
        "example",
        "project",
        "experience",
        "problem",
        "solution",
        "result",
        "challenge",
        "implemented",
        "developed",
        "improved",
        "testing",
        "team",
        "learned"
    ]

    found_keywords = [
        word for word in useful_keywords
        if word.lower() in answer.lower()
    ]

    # -----------------------------------------
    # Score calculation
    # -----------------------------------------

    score = 40

    # Answer length
    if word_count >= 50:
        score += 25
    elif word_count >= 30:
        score += 18
    elif word_count >= 15:
        score += 10
    else:
        score -= 10

    # Detailed keywords
    score += min(len(found_keywords) * 3, 20)

    # Specific examples
    if "example" in answer.lower():
        score += 5

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    # -----------------------------------------
    # Determine answer strength
    # -----------------------------------------

    if score >= 75:
        strength = "strong"

    elif score >= 50:
        strength = "medium"

    else:
        strength = "weak"

    # -----------------------------------------
    # Strengths
    # -----------------------------------------

    strengths = []

    if word_count >= 30:
        strengths.append(
            "The answer provides reasonable detail."
        )

    if found_keywords:
        strengths.append(
            "The answer contains relevant interview concepts."
        )

    if "example" in answer.lower():
        strengths.append(
            "The candidate included a specific example."
        )

    if word_count >= 50:
        strengths.append(
            "The answer demonstrates good explanation depth."
        )

    if not strengths:
        strengths.append(
            "The candidate attempted to address the question."
        )

    # -----------------------------------------
    # Weaknesses
    # -----------------------------------------

    weaknesses = []

    if word_count < 15:
        weaknesses.append(
            "The answer is too short and needs more explanation."
        )

    if word_count < 30:
        weaknesses.append(
            "Add more specific details to demonstrate understanding."
        )

    if "example" not in answer.lower():
        weaknesses.append(
            "Consider supporting the answer with a real example."
        )

    if len(found_keywords) < 2:
        weaknesses.append(
            "The answer could contain more relevant technical or practical details."
        )

    # -----------------------------------------
    # Final analysis message
    # -----------------------------------------

    if strength == "strong":

        analysis = (
            "Strong answer. The response shows good detail, "
            "relevant understanding, and enough information for "
            "the interviewer to explore deeper."
        )

    elif strength == "medium":

        analysis = (
            "Moderate answer. The candidate has addressed the "
            "question, but the response could be more specific "
            "and detailed."
        )

    else:

        analysis = (
            "Weak answer. The response needs more explanation, "
            "specific details, and preferably a practical example."
        )

    return {
        "score": score,
        "strength": strength,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "analysis": analysis
    }
