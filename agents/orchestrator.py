import asyncio
import os
from groq import Groq
from agents.reviewer import run_reviewer
from agents.tester import run_tester
from agents.improver import run_improver
from models.schemas import CodeReviewRequest, AgentResult, CodeReviewResponse

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def orchestrate(request: CodeReviewRequest) -> CodeReviewResponse:
    loop = asyncio.get_event_loop()

    # Run reviewer and tester in parallel
    review_task = loop.run_in_executor(
        None, run_reviewer, request.code, request.language, request.focus
    )
    tester_task = loop.run_in_executor(
        None, run_tester, request.code, request.language
    )

    review_output, tests_output = await asyncio.gather(review_task, tester_task)

    # Improver runs after reviewer
    improved_output = await loop.run_in_executor(
        None, run_improver, request.code, request.language, review_output
    )

    # Final summary
    summary_msg = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"""Summarize this code review in 3 bullet points.
Be concise and actionable.

Review: {review_output[:500]}"""
        }]
    )

    return CodeReviewResponse(
        review=AgentResult(agent="Reviewer", output=review_output),
        tests=AgentResult(agent="Tester", output=tests_output),
        improved_code=AgentResult(agent="Improver", output=improved_output),
        summary=summary_msg.choices[0].message.content
    )