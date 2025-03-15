from typing import List, Any, Dict
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.email_analysis import EmailAnalysisTool, SuggestEmailImprovementsTool

class Email:
    """Class representing an email to be reviewed."""
    def __init__(
        self,
        subject: str,
        content: str,
        sender: str,
        recipients: List[str],
        context: str = "professional"
    ):
        self.subject = subject
        self.content = content
        self.sender = sender
        self.recipients = recipients
        self.context = context

class EmailReviewerAgent(BaseAgent):
    """
    Agent specialized in reviewing emails for tone, clarity, and professionalism.
    """
    
    def __init__(
        self,
        config: Config,
        verbose: bool = False
    ):
        """Initialize the Email Reviewer agent."""
        super().__init__(
            config=config,
            role="Email Communication Expert",
            goal="Review and improve email communication for clarity, tone, and effectiveness",
            backstory="""You are an expert in professional communications, with deep knowledge of
            email etiquette, tone management, and effective business writing. You can identify subtle
            issues in email communication and provide actionable suggestions for improvement.""",
            verbose=verbose
        )
    
    def get_tools(self) -> List[Any]:
        """Get the tools available to this agent."""
        return [
            EmailAnalysisTool(),
            SuggestEmailImprovementsTool()
        ]
    
    async def review_email(self, email: Email) -> Dict[str, Any]:
        """
        Review an email for tone, clarity, and potential issues.
        
        Args:
            email (Email): The email to review.
            
        Returns:
            Dict[str, Any]: Analysis and suggestions for the email.
        """
        task = f"""
        Review the following email for tone, clarity, professionalism, and effectiveness:
        
        SUBJECT: {email.subject}
        FROM: {email.sender}
        TO: {', '.join(email.recipients)}
        CONTEXT: {email.context}
        
        CONTENT:
        {email.content}
        
        Provide a detailed analysis including:
        1. Overall impression and effectiveness
        2. Tone assessment (Is it appropriate for the context?)
        3. Clarity and structure
        4. Specific suggestions for improvement
        5. Potential misunderstandings or issues the recipient might have
        
        Use the email analysis tools to evaluate the content and suggest improvements.
        """
        
        result = await self.execute_task(task)
        
        # Format the result as a dictionary
        return {
            "email_id": hash(email.content),
            "subject": email.subject,
            "analysis": result,
            "context": email.context,
        } 