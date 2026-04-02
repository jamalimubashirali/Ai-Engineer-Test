# Advertising Agency AI Engineer Assessment

Welcome to the AI Engineer Candidate Assessment repository! This project demonstrates a production-tier approach to integrating Large Language Models (LLMs) into an advertising agency's workflow.

The entire assessment has been refactored into a **modular, maintainable, and robust architecture** that adheres strictly to best practices in AI engineering.

---

## 🏗️ Architecture & Philosophy

Across all tasks, this codebase enforces strict architectural consistency:

1. **Service Layer Isolation (`services/`)**
   LLM interaction is isolated from API endpoints or CLI logic. All LLM calls use **LangChain's LCEL** (`prompt | llm | parser`) for robust execution, retry mechanics, and clear declarative flows.
2. **Pydantic Validation (`models/`)**
   Every single LLM interaction uses a `JsonOutputParser` paired with a strict Pydantic model. This guarantees that responses are always perfectly validated, type-safe JSON objects ready for frontend consumption.
3. **Global Configuration (`config/`)**
   Instead of hardcoding environment values per script, all paths hook back to a centralized `config/env.py` validation layer with fail-fast `.env` checks.
4. **API First (`routers/` & `main.py`)**
   Web servers are built using **FastAPI** with highly documented routes and separation of concerns.

### 🧠 Model Selection

_Note: Due to the non-availability of OpenAI and Anthropic API credits, all models in this project use free-tier alternatives._

To ensure reviewers can run this project locally with zero API costs, all default configurations have been migrated to use **free open-weights models via OpenRouter** and local databases:

- **Chat/Text:** `meta-llama/llama-3.3-70b-instruct:free`
- **Vision:** `nvidia/nemotron-nano-12b-v2-vl:free`
- **Embeddings (RAG):** `all-MiniLM-L6-v2` (Running entirely locally via `sentence-transformers` — zero cost).

---

## 🚀 Quick Start & Setup

**This entire project relies on a single, unified virtual environment and global dependency list.**

1. **Root Configuration & Setup**
   From the project root directory, initialize the environment and install all packages:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate      # Windows
   # source venv/bin/activate   # Mac/Linux
   pip install -r requirements.txt

   cp .env.example .env
   # Add your OPENROUTER_API_KEY inside .env
   ```

2. **Run Any Task**
   Navigate to the respective task folder with your virtual environment still activated, and execute the commands below. Ensure you are using `python -m` to enforce the virtual environment's executables.

---

## 📂 Task Breakdown

### Task 1.1 — AI Copywriting API

A command-line script utilizing `ChatOpenAI` and LCEL to produce multiple structured variations of ad copy (headlines, taglines, body, CTA) from a user brief. Employs targeted exponential back-off catching `RateLimitError` distinct from `AuthenticationError`.

```bash
cd task_1_1_copywriting_api
python copy_generator.py "New luxury perfume for men, brand name: Noir, target: 30-45 year old professionals"
```

### Task 1.2 — Advanced Prompt Engineering

A detailed markdown audit comparing weak prompts with refactored, highly advanced prompting patterns. Includes documentation on Chain-of-Thought, XML fencing, targeted persona injection, and few-shot formatting, alongside side-by-side LLM output validation.

- **File:** `task_1_2_prompt_engineering/prompts_and_explanations.md`

### Task 2.1 — Campaign Brief Analyzer

A FastAPI microservice that extracts deeply targetable structure (audiences, channels, risk flags) from plain text or **uploaded PDFs**.

- Includes a **Bonus SSE Streaming Endpoint** (`/stream`) yielding token-by-token generation for interactive frontends.
- Includes a **Dockerfile** for robust container execution.

```bash
cd task_2_1_campaign_brief_analyzer
python -m uvicorn main:app --reload
# View Swagger UI at http://localhost:8000/docs
```

### Task 2.2 — AI Image Description & Auto-Tagging

A batch processing vision script. Uses `HumanMessage` multimodality to feed base64-encoded images to the LLaMA Vision model. Safely catches format mismatches and enforces minimum valid logic via strict Pydantic schemas. Includes fallback placeholders on failure so the batch never crashes.

```bash
cd task_2_2_image_tagging
# Place test images in the images/ directory
python image_tagger.py
```

### Task 2.3 — RAG-Based Campaign Knowledge Bot

A local RAG engine executing over full, robust markdown files of internal brand guidelines and case studies. Employs `ChromaDB` for local vector storage. Built with rigorous prompt boundaries forcing the bot to respond with precise `answer`, `source`, and exact verbatim `quote` extractions from the context—while safely refusing irrelevant questions.
Includes both a **CLI script** and a **Streamlit Web Dashboard**.

```bash
cd task_2_3_rag_chatbot
streamlit run streamlit_app.py
```

### Section 3 — Speed Tasks

This section covers rapid problem-solving, architectural thinking, and prompt engineering exercises:

- **Q1 (Retry Logic):** `section_3_speed_tasks/q1_retry.py` — A production-grade exponential back-off HTTP wrapper demonstrating robust API resilience.
- **Q2 (RAG Debugging):** _Not solved_. The assessment brief asked to debug a provided RAG script, but no script was provided in the repository to debug.
- **Q3 (System Prompt):** `section_3_speed_tasks/q3_system_prompt.txt` — An advanced, defense-in-depth system prompt utilizing chain-of-thought and strict constraints to eliminate hallucinations.
- **Q4 (Image Evaluation):** `section_3_speed_tasks/q4_image_evaluation.md` — An analytical comparison and evaluation of AI evaluation methodologies.
- **Q5 (Architecture):** `section_3_speed_tasks/q5_architecture.md` — A system design overview detailing scalability and orchestration for enterprise AI deployments.

---

_Thank you for reviewing. 🚀_
