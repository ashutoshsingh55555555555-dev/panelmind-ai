# PanelMind AI

<p align="center">
	<img src="assets/logo.png" alt="PanelMind AI logo" width="180">
</p>

## Adaptive AI Interview Panel Simulator

PanelMind AI is an interactive mock interview simulator that behaves more like a real interview panel than a fixed questionnaire. It analyzes each answer, identifies its strength, and chooses a follow-up question that matches the candidate's depth.

<p align="center">
	<a href="https://panelmind-ai-i3q9wokddjl5b2z67f4ryn.streamlit.app/">Open the live interview simulator</a>
</p>

> Strong answers get deeper questions. Vague answers get clarification. Reasonable answers get practical probing.

## Problem

Most mock-interview tools ask the same pre-written questions in the same order. Real interviewers listen to what a candidate says and follow up on the gaps, choices, and evidence in that answer.

For example, if a candidate says, "I used React for the frontend," a real panel may ask why React was chosen, how state was managed, and what trade-offs were accepted. PanelMind AI is designed to create that pressure in a repeatable practice environment.

## What It Does

- Supports Technical, HR, and General interview rounds
- Offers 10 base questions per interview mode
- Scores answers using detail, evidence, examples, and relevant concepts
- Classifies responses as weak, medium, or strong
- Generates adaptive follow-ups based on answer signals and difficulty
- Detects topics such as React, databases, teamwork, bugs, and trade-offs
- Provides strengths, weaknesses, analysis, and improvement advice
- Uses the STAR framework for behavioral interview guidance
- Includes optional voice recording and speech-to-text input
- Produces a question-by-question final performance report

## Adaptive Interview Flow

```text
Choose interview mode
	|
	v
Ask base question
	|
	v
Analyze answer quality and topics
	|
	+--> Weak answer   -> Clarifying follow-up
	+--> Medium answer -> Example and reasoning follow-up
	+--> Strong answer -> Trade-off and deeper challenge
	|
	v
Generate personalized feedback
	|
	v
Build final interview report
```

## Example

**Candidate answer**

> I used React for the frontend and Redux for state management.

**Adaptive follow-up**

> Why did you choose that frontend approach over a simpler option, and how did you manage state across components?

This tests reasoning and depth instead of only checking whether the answer contains a technology keyword.

## Visual Preview

The project logo is included in [`assets/logo.png`](assets/logo.png). Try the complete interactive experience in the [live demo](https://panelmind-ai-i3q9wokddjl5b2z67f4ryn.streamlit.app/): choose an interview mode, answer a question, and continue through the adaptive follow-up flow.

## Tech Stack

- **Python**
- **Streamlit** for the interactive web interface
- **Rule-based analysis engine** for transparent scoring and feedback
- **SpeechRecognition** for optional voice transcription
- **Streamlit Community Cloud** for deployment

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ashutoshsingh55555555555-dev/panelmind-ai.git
cd panelmind-ai
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## How To Use

1. Select Technical, HR, or General Interview from the sidebar.
2. Choose between 3 and 10 base questions.
3. Optionally enable Voice Mode and record an answer.
4. Type or review your answer in the response box.
5. Select **Analyze My Answer**.
6. Read the score, strengths, gaps, and personalized feedback.
7. Answer the adaptive follow-up question.
8. Review the final interview report after the round ends.

## Project Structure

```text
panelmind-ai/
├── app.py                 # Streamlit UI and interview session flow
├── requirements.txt       # Runtime dependencies
├── assets/
│   └── logo.png           # Project asset
└── utils/
    ├── analyzer.py        # Answer scoring and strength classification
    ├── feedback.py        # Personalized coaching messages
    ├── questions.py       # Question banks and adaptive follow-ups
    └── voice.py           # Optional audio transcription
```

## Deployment

The project is ready for Streamlit Community Cloud deployment:

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Choose **Create app** and **Deploy from repo**.
3. Select `ashutoshsingh55555555555-dev/panelmind-ai`.
4. Set branch to `main`.
5. Set main file to `app.py`.
6. Deploy.

Live demo: [PanelMind AI](https://panelmind-ai-i3q9wokddjl5b2z67f4ryn.streamlit.app/)

## Voice Mode Note

Voice Mode uses the browser microphone through Streamlit's audio input and sends the recording to speech recognition for transcription. A working microphone and internet connection are required for transcription. Typed answers remain available as a fallback.

## Current Limitations

- The scoring engine is transparent and rule-based rather than a fully trained language model.
- Speech transcription depends on an external recognition service.
- Interview history is stored in the active Streamlit session and is not persisted to a database.
- Answers are not currently customized to a specific job description or resume.

## Future Scope

- Resume and job-description-aware question generation
- LLM-based semantic scoring with explainable rubrics
- Coding editor and test-case based technical rounds
- Speaking pace, filler-word, and confidence analysis
- Persistent user profiles and progress tracking
- Multi-panel interviewer personas

## Hackathon Value

PanelMind AI focuses on a clear gap in interview preparation: candidates need practice responding to follow-up pressure, not just memorizing answers. The project combines an accessible interface, explainable feedback, adaptive questioning, and optional voice practice into one deployable workflow.

## License

This project is currently provided for educational and hackathon use.
