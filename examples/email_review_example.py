import asyncio
from src.core.config import Config
from src.agents import AgentFactory, Email

async def main():
    # Initialize configuration
    config = Config.from_yaml()
    
    # Create email reviewer agent using the factory
    reviewer = AgentFactory.create_agent("email_reviewer", config=config)
    
    # Sample emails to review
    sample_emails = [
        Email(
            subject="URGENT: Project Deadline Update!!",
            content="""
            Hi team,
            
            We NEED to get this project done ASAP!! The deadline has been moved up
            and everything needs to be completed by next week! This is super urgent
            and I need everyone to drop what they're doing and focus on this RIGHT NOW!!
            
            Let me know immediately if you can't make this happen!
            
            Thanks,
            Manager
            """,
            sender="manager@company.com",
            recipients=["team@company.com"],
            context="internal_team"
        ),
        Email(
            subject="Meeting Request: Partnership Discussion",
            content="""
            Dear Mr. Johnson,
            
            I hope this email finds you well. I am writing to request a meeting to discuss 
            potential partnership opportunities between our organizations. Our company has 
            developed innovative solutions in the AI space that I believe could create 
            significant synergies with your operations.
            
            I would greatly appreciate the opportunity to schedule a 30-minute video call 
            at your convenience next week to explore this further. I can provide a detailed 
            agenda and additional materials in advance of our discussion.
            
            Looking forward to your response.
            
            Best regards,
            Sarah Chen
            Business Development Manager
            """,
            sender="sarah.chen@company.com",
            recipients=["mjohnson@partner.com"],
            context="external_business"
        )
    ]
    
    # Review each email
    for i, email in enumerate(sample_emails, 1):
        print(f"\nReviewing Email {i}:")
        print("-" * 50)
        print(f"Subject: {email.subject}")
        print(f"Context: {email.context}")
        print("-" * 50)
        
        try:
            result = await reviewer.review_email(email)
            print("\nReview Results:")
            print(result["review_result"])
        except Exception as e:
            print(f"Error during review: {str(e)}")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 