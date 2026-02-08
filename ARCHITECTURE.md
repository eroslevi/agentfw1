# Framework Architecture Diagram

Visual representation of the Intelligent Multi-Agentic System Framework architecture.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRAMEWORK CORE COMPONENTS                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐   │
│  │ SPECIFICATIONS   │  │    PROMPTS       │  │   CORE MODULES  │   │
│  │ (Templates)      │  │  (LLM Guidance)  │  │   (Python)      │   │
│  ├──────────────────┤  ├──────────────────┤  ├─────────────────┤   │
│  │ • USR_SPEC_TMP   │  │ • ARCH_PROMPT    │  │ • llm_client.py │   │
│  │ • ARCH_SPEC_TMP  │  │ • TECH_PROMPT    │  │ • chk.py        │   │
│  │ • TECH_SPEC_TMP  │  │ • CODE_PROMPT    │  │ • __init__.py   │   │
│  │ • TEST_SPEC_TMP  │  │ • TEST_SPEC_...  │  │                 │   │
│  │                  │  │ • TEST_CODE_...  │  │                 │   │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘   │
│           │                    │                     │               │
└───────────┼────────────────────┼─────────────────────┼───────────────┘
            │                    │                     │
            ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AZURE OPENAI LLM                             │
│                  (Specification & Code Generation)                   │
└─────────────────────────────────────────────────────────────────────┘
            │                    │                     │
            ▼                    ▼                     ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ ARCH_SPEC   │      │ TECH_SPEC   │      │ TEST_SPEC   │
    │ (Generated) │      │ (Generated) │      │ (Generated) │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                     │
           └────────────────────┼─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │  SRC (Source Code)      │
                    │  TST (Test Suite)       │
                    │  (Both Generated)       │
                    └─────────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────┐
                       │  CHK Mechanism   │
                       │  (Test & Fix)    │
                       └────────┬─────────┘
                                │
                    ┌───────────┴────────────┐
                    ▼                        ▼
                 ✓ PASS              ✗ FAIL (auto-fix)
                    │                        │
                    │                        ▼
                    │                   Fix attempts
                    │                   (up to 3)
                    │                        │
                    └───────────┬────────────┘
                                ▼
                        ┌─────────────────┐
                        │   Final Result  │
                        │  ✓ System Ready │
                        └─────────────────┘
```

## Data Flow Through Generation Pipeline

```
USER INPUT
    │
    ├─ Writes ──┐
    │           ▼
    │      USR_SPEC (Markdown)
    │      • Goals
    │      • Requirements
    │      • Input/Output specs
    │      • Success criteria
    │           │
    │           ▼ (ARCH_PROMPT)
    │           │
    │           ├─ Input: USR_SPEC
    │           ├─ Template: ARCH_SPEC_TMP
    │           ├─ LLM: Azure OpenAI
    │           │
    │           ▼
    │      ARCH_SPEC (Markdown)
    │      • Agents definition
    │      • Tools definition
    │      • Data flow
    │      • Integration points
    │           │
    │           ├────────────────────────────────────┐
    │           │                                    │
    │           ▼ (TECH_PROMPT)               ▼ (TEST_SPEC_PROMPT)
    │           │                             │
    │           ├─ Input: ARCH_SPEC           ├─ Input: ARCH_SPEC + TECH_SPEC
    │           ├─ Template: TECH_SPEC_TMP    ├─ Template: TEST_SPEC_TMP
    │           ├─ LLM: Azure OpenAI          ├─ LLM: Azure OpenAI
    │           │                             │
    │           ▼                             │
    │      TECH_SPEC (Markdown)               │
    │      • Python Classes                   │
    │      • Method Signatures                │
    │      • Type Hints                       │
    │      • Utilities                        │
    │           │                             │
    │           │                (Sequential) │
    │           │                  dependency │
    │           ├──────────────────────────────→
    │           │                             │
    │           │                             ▼
    │           │                        TEST_SPEC
    │           │                        • Test cases
    │           │                        • Assertions
    │           │                        • Coverage
    │           │                        • Edge cases
    │           │                             │
    │           ▼ (CODE_PROMPT)               ▼ (TEST_CODE_PROMPT)
    │           │                             │
    │           ├─ Input: TECH_SPEC           ├─ Input: TEST_SPEC
    │           ├─ Prompt: CODE_PROMPT        ├─ Prompt: TEST_CODE_PROMPT
    │           ├─ LLM: Azure OpenAI          ├─ LLM: Azure OpenAI
    │           │                             │
    │           ▼                             ▼
    │      SRC (Source Code)              TST (Test Suite)
    │      • agents/                       • tests/unit/
    │      • tools/                        • tests/integration/
    │      • utils/                        • tests/e2e/
    │      • graph.py                      • conftest.py
    │      • main.py                       • fixtures/
    │           │                             │
    │           └──────────┬──────────────────┘
    │                      │
    │                      ▼ (Save to generated_systems/[system_name]/)
    │                      │
    │                      ▼
    │                 RUN CHK
    │                 • Execute tests (TST)
    │                 • Check results
    │                 • If fail: Generate fixes
    │                 • Rerun tests (retry up to 3x)
    │                 • Report status
    │                      │
    └──────────────────────┴──────────────┐
                                          ▼
                                  ✓ SYSTEM READY
```

## Framework Module Dependencies

```
┌────────────────────────────────────────────────────────┐
│  framework/core/llm_client.py                          │
├────────────────────────────────────────────────────────┤
│ Dependencies:                                           │
│  - openai.AzureOpenAI                                  │
│  - typing (Type hints)                                 │
│  - os (Environment variables)                          │
│                                                        │
│ Exports:                                               │
│  - class AzureLLMClient                               │
│  - function get_llm_client()                          │
│                                                        │
│ Usage:                                                 │
│  from framework.core import get_llm_client            │
│  llm = get_llm_client()                               │
│  spec = llm.generate_specification(...)               │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  framework/core/chk.py                                 │
├────────────────────────────────────────────────────────┤
│ Dependencies:                                           │
│  - subprocess (Run pytest)                             │
│  - pathlib.Path (File paths)                           │
│  - json (Report serialization)                         │
│  - datetime (Timestamps)                               │
│  - typing (Type hints)                                 │
│  - llm_client (For LLM fixes)                          │
│                                                        │
│ Exports:                                               │
│  - class CheckMechanism                               │
│  - function run_check()                               │
│                                                        │
│ Usage:                                                 │
│  from framework.core import run_check                 │
│  success, summary = run_check(system_path, ...)       │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  framework/core/__init__.py                            │
├────────────────────────────────────────────────────────┤
│ Imports:                                               │
│  - from .llm_client import AzureLLMClient, get_llm_client
│  - from .chk import CheckMechanism, run_check        │
│                                                        │
│ __all__ = [                                            │
│   'AzureLLMClient',                                    │
│   'get_llm_client',                                    │
│   'CheckMechanism',                                    │
│   'run_check'                                          │
│ ]                                                      │
└────────────────────────────────────────────────────────┘
```

## Directory Structure Visualization

```
agentfw1/                                    ← Framework root
│
├── README.md                                ← Main documentation
├── QUICKSTART.md                            ← Quick start guide
├── WORKFLOW.md                              ← Workflow diagrams
├── FRAMEWORK_COMPONENTS.md                  ← Component index
├── EXAMPLE_USR_SPEC.md                      ← Example specification
├── DELIVERABLES.md                          ← This implementation
├── requirements.txt                         ← Dependencies
│
├── framework/                               ← Framework core
│   ├── specifications/                      ← Specification templates
│   │   ├── USR_SPEC_TEMPLATE.md
│   │   ├── ARCH_SPEC_TEMPLATE.md
│   │   ├── TECH_SPEC_TEMPLATE.md
│   │   └── TEST_SPEC_TEMPLATE.md
│   │
│   ├── prompts/                            ← LLM guidance prompts
│   │   ├── ARCH_PROMPT.md
│   │   ├── TECH_PROMPT.md
│   │   ├── CODE_PROMPT.md
│   │   ├── TEST_SPEC_PROMPT.md
│   │   └── TEST_CODE_PROMPT.md
│   │
│   └── core/                               ← Python implementation
│       ├── __init__.py
│       ├── llm_client.py                   ← Azure OpenAI interface
│       └── chk.py                          ← Test & fix mechanism
│
└── generated_systems/                      ← Generated systems (empty)
    └── [system_name]/                      ← Populated by framework
        ├── specs/                          ← Specification files
        ├── src/                            ← Source code
        ├── tests/                          ← Test suite
        ├── requirements.txt
        └── README.md
```

## Specification Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  LEVEL 1: USER REQUIREMENTS                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  USR_SPEC                                                  │  │
│  │  What: High-level goals and requirements                  │  │
│  │  Who: User writes                                         │  │
│  │  Format: Markdown with clear sections                     │  │
│  │  Content:                                                 │  │
│  │  • Project description                                    │  │
│  │  • Primary goals                                          │  │
│  │  • Key requirements                                       │  │
│  │  • Input/output specifications                            │  │
│  │  • Success criteria                                       │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  LEVEL 2: SYSTEM ARCHITECTURE                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  ARCH_SPEC                                                 │  │
│  │  What: How agents and tools interact                       │  │
│  │  Generated: ARCH_PROMPT + USR_SPEC → LLM                  │  │
│  │  Format: Markdown with detailed sections                   │  │
│  │  Content:                                                 │  │
│  │  • Agent definitions and interactions                      │  │
│  │  • Tool definitions and parameters                         │  │
│  │  • Data flow architecture                                  │  │
│  │  • Error handling strategies                               │  │
│  │  • Integration points with external systems                │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
      ┌──────────────────────┐  ┌─────────────────────┐
      │  LEVEL 3A:           │  │  LEVEL 3B:          │
      │  TECHNICAL DETAILS   │  │  TEST STRATEGY      │
      │  ┌────────────────┐  │  │  ┌───────────────┐  │
      │  │  TECH_SPEC    │  │  │  │  TEST_SPEC    │  │
      │  │  Generated by:│  │  │  │  Generated by: │  │
      │  │  TECH_PROMPT+ │  │  │  │  TEST_SPEC_..│  │
      │  │  ARCH_SPEC    │  │  │  │  + ARCH_SPEC │  │
      │  │               │  │  │  │  + TECH_SPEC │  │
      │  │  Content:     │  │  │  │               │  │
      │  │  • Classes    │  │  │  │  Content:     │  │
      │  │  • Methods    │  │  │  │  • Unit tests │  │
      │  │  • Signatures │  │  │  │  • Integ tests│  │
      │  │  • Types      │  │  │  │  • E2E tests  │  │
      │  │  • Utilities  │  │  │  │  • Edge cases │  │
      │  └────────────────┘  │  │  └───────────────┘  │
      └──────────────────────┘  └─────────────────────┘
                    │                   │
                    ▼                   ▼
      ┌──────────────────────┐  ┌─────────────────────┐
      │  LEVEL 4A: CODE      │  │  LEVEL 4B: TESTS    │
      │  ┌────────────────┐  │  │  ┌───────────────┐  │
      │  │  SRC           │  │  │  │  TST          │  │
      │  │  Generated by: │  │  │  │  Generated by:│  │
      │  │  CODE_PROMPT + │  │  │  │  TEST_CODE..+│  │
      │  │  TECH_SPEC     │  │  │  │  TEST_SPEC   │  │
      │  │                │  │  │  │               │  │
      │  │  Files:        │  │  │  │  Files:       │  │
      │  │  • agents/     │  │  │  │  • unit/      │  │
      │  │  • tools/      │  │  │  │  • integration│  │
      │  │  • utils/      │  │  │  │  • e2e/       │  │
      │  │  • graph.py    │  │  │  │  • fixtures/  │  │
      │  │  • main.py     │  │  │  │  • conftest.p│  │
      │  └────────────────┘  │  │  └───────────────┘  │
      └──────────────────────┘  └─────────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  LEVEL 5: VALIDATION                                             │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  CHK (Check Mechanism)                                     │  │
│  │  Process:                                                  │  │
│  │  1. Run test suite (TST)                                  │  │
│  │  2. Check results                                          │  │
│  │     ✓ All pass → Success, system ready                    │  │
│  │     ✗ Some fail → Auto-fix (optional)                     │  │
│  │  3. Generate fix suggestions using LLM                    │  │
│  │  4. Rerun tests                                            │  │
│  │  5. Repeat up to 3 times                                   │  │
│  │  6. Report final status                                    │  │
│  │                                                            │  │
│  │  Output: ✓ System Ready or ✗ Manual fixes needed          │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## Integration Points

```
┌─────────────────────────────────────────────────────────┐
│  External Systems                                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Azure OpenAI                                           │
│  ├─ LLM for generation (ARCH, TECH, CODE, TEST)       │
│  ├─ LLM for fix suggestions (CHK)                       │
│  └─ API: AzureOpenAI SDK                               │
│                                                         │
│  Python Ecosystem                                       │
│  ├─ LangGraph (Agent orchestration)                    │
│  ├─ LangChain (LLM framework)                          │
│  ├─ pytest (Testing)                                    │
│  └─ Standard library                                    │
│                                                         │
│  Git/Version Control (Optional)                         │
│  ├─ Track specifications                               │
│  ├─ Track generated code                               │
│  └─ Maintain history                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Generation Process: Sequential & Parallel Paths

```
START
  │
  ├─ User creates USR_SPEC (20 min)
  │
  ├─ ARCH_PROMPT (Input: USR_SPEC)
  │
  ▼
  ARCH_SPEC (2 min)
  │
  └─┬────────────────────────────────────┐
    │                                    │
    ▼ (SEQUENTIAL)              ▼ (Dependent on TECH_SPEC)
    │                                    │
    TECH_PROMPT                 TEST_SPEC_PROMPT
    (Input: ARCH_SPEC)         (Input: ARCH_SPEC + TECH_SPEC)
    │                                    │
    ▼                                    │
    TECH_SPEC (2 min)                    │
    │                                    │
    ├────────────────────────────────────→
    │                                    │
    │ (Dependency satisfied)             │
    │                                    ▼
    │                              TEST_SPEC (2 min)
    │                                    │
    ▼ (CODE_PROMPT)                  ▼ (TEST_CODE_PROMPT)
    │                                    │
    (Input: TECH_SPEC)          (Input: TEST_SPEC)
    │                                    │
    ▼                                    ▼
    SRC (source code) (2 min)  TST (test suite) (2 min)
    │                                    │
    └────────────────┬───────────────────┘
                     ▼
             Organize in
             generated_systems/[system]/
                     │
                     ▼
             RUN CHK
             (Test & Fix)
                     │
          ┌─────┴──────┐
          ▼            ▼
    All Pass      Some Fail
          │            │
          ▼            ▼ (if auto_fix=True)
       ✓ READY    LLM Fix
                 Suggestions
                      │
                      ▼
                   Apply Fixes
                      │
                      ▼
                  Rerun Tests
                      │
               ┌──────┴────────┐
               ▼               ▼
             PASS        FAIL (retry)
               │               │
               ▼               ▼
            ✓ READY      Max retries?
                          │
                    Yes ──┴── No
                    │         │
                    ▼         ▼
                  DONE    Try again
                          (up to 3x)

END
```

---

This architecture ensures a structured, systematic approach to generating intelligent multi-agentic systems with proper specification at each level and comprehensive testing throughout.
