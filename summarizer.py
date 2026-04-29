"""
Meeting analysis using Groq API — free tier, no credit card required.
Sign up at https://console.groq.com to get a free API key.
Model: llama-3.3-70b-versatile (fast, free, powerful)
"""

import os
import json
import re
from groq import Groq

def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Get a free key at https://console.groq.com "
            "then set it: export GROQ_API_KEY=your_key_here"
        )
    return Groq(api_key=api_key)

SYSTEM_PROMPT = """You are an expert meeting analyst. When given a meeting transcript, extract and structure the following information.

Return ONLY valid JSON — no preamble, no markdown fences, no extra text. Use this exact schema:

{
  "summary": "3-5 sentence executive summary of the meeting",
  "key_topics": ["topic 1", "topic 2", "..."],
  "decisions": [
    {"decision": "what was decided", "context": "brief context or rationale"}
  ],
  "action_items": [
    {
      "task": "description of the task",
      "owner": "person responsible (or 'Unassigned')",
      "deadline": "deadline if mentioned (or 'Not specified')",
      "priority": "High / Medium / Low"
    }
  ],
  "follow_up_questions": ["question 1", "question 2"],
  "sentiment": "Positive / Neutral / Mixed / Tense",
  "meeting_type": "e.g. Planning, Retrospective, Standup, Client Call, etc."
}"""

def analyze_meeting(transcript: str, meeting_title: str, meeting_date: str, participants: str) -> dict:
    client = get_client()

    user_prompt = f"""Meeting Title: {meeting_title}
Date: {meeting_date}
Participants: {participants}

TRANSCRIPT:
{transcript}

Analyze the above meeting transcript and return structured JSON as instructed."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=2048
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if model wrapped anyway
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    result = json.loads(raw)
    result["meeting_title"] = meeting_title
    result["meeting_date"] = meeting_date
    result["participants"] = participants
    return result
