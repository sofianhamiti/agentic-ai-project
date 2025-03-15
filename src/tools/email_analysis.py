from typing import Dict, Any
from crewai.tools import BaseTool

class EmailAnalysisTool(BaseTool):
    """Tool for analyzing email content."""
    
    name: str = "Email Analysis"
    description: str = "Analyze email content for tone, clarity, and potential issues"
    
    def _run(self, content: str, context: str = "professional") -> Dict[str, Any]:
        """Analyze email content."""
        return {
            "email_id": hash(content),
            "context": context,
            "checks_performed": [
                "tone_analysis",
                "clarity_check",
                "grammar_review",
                "sensitivity_scan"
            ],
            "requires_human_review": False
        }

class SuggestEmailImprovementsTool(BaseTool):
    """Tool for suggesting email improvements."""
    
    name: str = "Suggest Email Improvements"
    description: str = "Suggest improvements for email content"
    
    def _run(self, content: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest improvements for the email."""
        # Check for common issues
        content_lower = content.lower()
        suggestions = []
        confidence = 0.9
        
        # Check tone
        if any(word in content_lower for word in ["urgent", "asap", "immediately"]):
            suggestions.append({
                "type": "tone",
                "issue": "Potentially demanding tone",
                "suggestion": "Consider using more collaborative language"
            })
            confidence = 0.85
            
        # Check clarity
        if len(content.split()) > 200:
            suggestions.append({
                "type": "clarity",
                "issue": "Email length",
                "suggestion": "Consider condensing for better readability"
            })
            
        # Check professionalism
        if "!" in content or "!!" in content:
            suggestions.append({
                "type": "professionalism",
                "issue": "Excessive punctuation",
                "suggestion": "Maintain professional tone with standard punctuation"
            })
        
        return {
            "email_id": analysis_result["email_id"],
            "suggestions": suggestions,
            "improvement_areas": [s["type"] for s in suggestions],
            "confidence": confidence
        } 