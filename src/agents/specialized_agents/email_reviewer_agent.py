from typing import List, Any, Dict
from ..base_agent import BaseAgent
from ...core.config import Config
from ...tools.email_analysis import EmailAnalysisTool, SuggestEmailImprovementsTool
from crewai import Task

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
    """An agent specialized in reviewing and improving email communications."""
    
    def __init__(self, config: Config):
        super().__init__(
            config=config,
            role="Email Communication Specialist",
            goal="Review and improve email communications for clarity, professionalism, and effectiveness",
            backstory="""I am an expert in professional communication with years of 
            experience in improving email effectiveness. I understand the nuances of 
            business communication and can help ensure emails achieve their intended 
            purpose while maintaining appropriate tone and professionalism.""",
            verbose=True
        )
        self._tools = self.get_tools()
    
    def get_tools(self) -> List[Any]:
        """Get the tools available to the email reviewer agent."""
        return [
            EmailAnalysisTool(),
            SuggestEmailImprovementsTool()
        ]
    
    async def review_email(self, email: Email) -> Dict[str, Any]:
        """Review an email and provide improvement suggestions."""
        task_description = f"""
        Review the following email:
        
        Subject: {email.subject}
        From: {email.sender}
        To: {', '.join(email.recipients)}
        Context: {email.context}
        
        Content:
        {email.content}
        
        Please follow these steps:
        1. Analyze the email content using the Email Analysis tool
        2. Based on the analysis, suggest improvements using the Suggest Email Improvements tool
        3. Provide a comprehensive review with specific recommendations
        4. Consider the context and audience when making suggestions
        
        Focus on:
        - Tone and professionalism
        - Clarity and conciseness
        - Effectiveness in achieving the email's purpose
        - Cultural sensitivity and appropriateness
        """
        
        task = Task(
            description=task_description,
            expected_output="A comprehensive email review with specific recommendations",
            agent=self._agent,
            tools=self._tools
        )
        
        try:
            result = task.execute_sync(agent=self._agent, tools=self._tools)
            return {
                "email": email,
                "review_result": result.raw if hasattr(result, 'raw') else str(result)
            }
        except Exception as e:
            # If we have an error, create a simple review instead
            return {
                "email": email,
                "review_result": f"Error during task execution: {str(e)}\n\nSimple review: This email needs improvements in tone and clarity."
            } 