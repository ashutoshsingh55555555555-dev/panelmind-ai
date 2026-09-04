
# utils/feedback.py


def generate_feedback(question, answer, analysis):
    """
    Generate personalized interview feedback
    based on the answer analysis.
    """

    score = analysis["score"]
    strength = analysis["strength"]
    strengths = analysis["strengths"]
    weaknesses = analysis["weaknesses"]

    # -----------------------------------------
    # Overall feedback
    # -----------------------------------------

    if strength == "strong":

        overall = (
            "Excellent response! Your answer shows good understanding "
            "and provides enough detail for an interviewer."
        )

        improvement = (
            "To make it even stronger, explain the reasoning behind "
            "your decisions and be ready for deeper follow-up questions."
        )

    elif strength == "medium":

        overall = (
            "Good attempt. You addressed the question, but your "
            "answer can be made more specific and structured."
        )

        improvement = (
            "Try to explain what you personally did, why you chose "
            "your approach, and what result you achieved."
        )

    else:

        overall = (
            "Your answer needs more depth. An interviewer may ask "
            "additional questions to understand your knowledge."
        )

        improvement = (
            "Give a clearer explanation, include a practical example, "
            "and explain your own contribution."
        )

    # -----------------------------------------
    # STAR Method suggestion
    # -----------------------------------------

    star_tip = (
        "For behavioral questions, try the STAR structure: "
        "Situation → Task → Action → Result."
    )

    # -----------------------------------------
    # Build final feedback
    # -----------------------------------------

    feedback = {
        "score": score,
        "overall": overall,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvement": improvement,
        "star_tip": star_tip
    }

    return feedback
