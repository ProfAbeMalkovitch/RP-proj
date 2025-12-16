"""
Pathway Calculator
Calculates student pathway based on quiz scores
"""

def calculate_pathway(quiz_scores: list) -> str:
    """
    Calculate pathway based on average quiz score
    
    Rules:
    - Basic: 0-49
    - Intermediate: 50-74
    - Accelerated: 75-100
    
    Args:
        quiz_scores: List of quiz scores (percentages)
    
    Returns:
        Pathway name: "Basic", "Intermediate", or "Accelerated"
    """
    if not quiz_scores or len(quiz_scores) == 0:
        return "Basic"  # Default to Basic if no scores
    
    average_score = sum(quiz_scores) / len(quiz_scores)
    
    if average_score < 50:
        return "Basic"
    elif average_score < 75:
        return "Intermediate"
    else:
        return "Accelerated"


def calculate_average_score(quiz_scores: list) -> float:
    """Calculate average score from quiz scores"""
    if not quiz_scores or len(quiz_scores) == 0:
        return 0.0
    return sum(quiz_scores) / len(quiz_scores)





































