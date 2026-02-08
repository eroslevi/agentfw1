# Framework Components Index

Complete reference guide to all files and components in the Intelligent Multi-Agentic System Framework.

## Root Directory Files

### README.md
**Purpose**: Main framework documentation  
**Contents**: Overview, workflow, usage guide, API reference, troubleshooting  
**When to read**: When getting started or needing detailed documentation  

### QUICKSTART.md
**Purpose**: Quick start guide for new users  
**Contents**: 5-minute setup, step-by-step first system, common patterns  
**When to read**: When you want to create your first system quickly  

### WORKFLOW.md
**Purpose**: Detailed workflow documentation with diagrams  
**Contents**: Process flow, detailed phases, decision points, feedback loops  
**When to read**: To understand the complete generation process  

### EXAMPLE_USR_SPEC.md
**Purpose**: Example user specification (USR_SPEC)  
**Contents**: Complete example for a document analysis system  
**When to read**: Before creating your own USR_SPEC to understand the format  

### requirements.txt
**Purpose**: Python package dependencies  
**Contents**: All packages needed to run the framework  
**When to use**: `pip install -r requirements.txt`  

---

## framework/specifications/

Markdown templates that define the structure of each specification type.

### USR_SPEC_TEMPLATE.md

**What it is**: Template for User System Specifications  
**Created by**: You (the user)  
**Input to**: ARCH_PROMPT  
**Contains**:
- Project title and description
- Primary goals and key requirements
- Input data types and expected output
- Constraints and success criteria

**Example sections**:
```markdown
# User System Specification
## Project Title
## Primary Goals
## Key Requirements
## Input Data / Context
## Expected Output
## Constraints and Limitations
## Success Criteria
```

### ARCH_SPEC_TEMPLATE.md

**What it is**: Template for Architectural Specifications  
**Created by**: ARCH_PROMPT (from USR_SPEC)  
**Input to**: TECH_PROMPT  
**Contains**:
- Agent definitions and interactions
- Tool definitions and functionality
- System data flow
- Error handling strategies
- Integration points

**Key sections**:
```markdown
# Architectural Specification
## Agents
  - Agent functionality and interactions
## Tools
  - Tool functionality and parameters
## System Data Flow
## Error Handling and Fallbacks
## Integration Points
```

### TECH_SPEC_TEMPLATE.md

**What it is**: Template for Technical Specifications  
**Created by**: TECH_PROMPT (from ARCH_SPEC)  
**Input to**: CODE_PROMPT, TEST_SPEC_PROMPT  
**Contains**:
- Python class definitions
- Method signatures with types
- Utility function specifications
- LangGraph configuration
- Dependencies and constants

**Key sections**:
```markdown
# Technical Specification
## Agent Implementation Details
## Tool Implementation Details
## Utility and Support Methods
## LangGraph Configuration
## Configuration and Constants
```

### TEST_SPEC_TEMPLATE.md

**What it is**: Template for Test Specifications  
**Created by**: TEST_SPEC_PROMPT (from ARCH_SPEC + TECH_SPEC)  
**Input to**: TEST_CODE_PROMPT  
**Contains**:
- Unit test cases with steps and assertions
- Integration test cases
- E2E test cases
- Edge case and error scenarios
- Performance tests
- Test data requirements

**Key sections**:
```markdown
# Test Specification
## Test Cases
  - Test ID, type, component under test
  - Description, steps, expected results
  - Assertions and postconditions
## Edge Cases and Error Scenarios
## Integration Tests
## Test Coverage Summary
```

---

## framework/prompts/

Prompt templates used to generate specifications and code via LLM.

### ARCH_PROMPT.md

**Purpose**: Generate ARCH_SPEC from USR_SPEC  
**Input**: User System Specification  
**Output**: Architectural Specification  
**What it does**:
- Translates user requirements into architectural design
- Identifies needed agents and their responsibilities
- Designs tool interfaces
- Plans data flows and integrations

**Usage**:
```python
arch_spec = llm.generate_specification(
    template=open("framework/prompts/ARCH_PROMPT.md").read(),
    context=usr_spec,
    spec_type="architectural specification"
)
```

### TECH_PROMPT.md

**Purpose**: Generate TECH_SPEC from ARCH_SPEC  
**Input**: Architectural Specification  
**Output**: Technical Specification  
**What it does**:
- Translates architecture into Python implementation details
- Defines class structures and method signatures
- Specifies exact parameter and return types
- Plans LangGraph configuration

**Usage**:
```python
tech_spec = llm.generate_specification(
    template=open("framework/prompts/TECH_PROMPT.md").read(),
    context=arch_spec,
    spec_type="technical specification"
)
```

### CODE_PROMPT.md

**Purpose**: Generate SRC (source code) from TECH_SPEC  
**Input**: Technical Specification  
**Output**: Production-ready Python source code  
**What it does**:
- Generates complete agent classes
- Generates complete tool classes
- Creates utility functions
- Builds LangGraph workflow
- Includes error handling and logging

**Usage**:
```python
src_code = llm.generate_from_prompt(
    system_prompt=open("framework/prompts/CODE_PROMPT.md").read(),
    user_prompt=tech_spec
)
```

### TEST_SPEC_PROMPT.md

**Purpose**: Generate TEST_SPEC from ARCH_SPEC + TECH_SPEC  
**Input**: Architectural and Technical Specifications  
**Output**: Test Specification  
**What it does**:
- Creates unit test cases for each component
- Designs integration tests for component interactions
- Plans E2E tests for complete workflows
- Defines edge cases and error scenarios
- Specifies performance test criteria

**Usage**:
```python
test_spec = llm.generate_specification(
    template=open("framework/prompts/TEST_SPEC_PROMPT.md").read(),
    context=f"{arch_spec}\n{tech_spec}",
    spec_type="test specification"
)
```

### TEST_CODE_PROMPT.md

**Purpose**: Generate TST (test code) from TEST_SPEC  
**Input**: Test Specification  
**Output**: Production-ready pytest test suite  
**What it does**:
- Generates pytest test functions
- Creates fixtures for test setup/teardown
- Generates mocks for external dependencies
- Creates test utilities and helpers
- Configures pytest.ini or pyproject.toml

**Usage**:
```python
test_code = llm.generate_from_prompt(
    system_prompt=open("framework/prompts/TEST_CODE_PROMPT.md").read(),
    user_prompt=test_spec
)
```

---

## framework/core/

Core Python modules providing framework functionality.

### llm_client.py

**Purpose**: Access Azure-hosted OpenAI LLM  
**Main class**: `AzureLLMClient`  

**Key methods**:
- `create_chat_completion()` - Generate completions
- `create_chat_completion_with_retries()` - Generate with automatic retries
- `generate_from_prompt()` - Simple prompt-based generation
- `generate_specification()` - Generate specifications (ARCH, TECH, TEST, etc.)

**Usage**:
```python
from framework.core import get_llm_client

llm = get_llm_client(
    azure_endpoint="https://...",
    api_key="..."
)

response = llm.generate_from_prompt(
    system_prompt="You are an expert...",
    user_prompt="Generate a..."
)
```

**Imports**:
- `openai.AzureOpenAI` - Azure OpenAI client
- Standard library: `os`, `typing`, `pathlib`

### chk.py

**Purpose**: Check (test and fix) generated systems  
**Main class**: `CheckMechanism`  

**Key methods**:
- `run_tests()` - Execute pytest test suite
- `parse_test_failures()` - Extract failure information
- `generate_fix_prompt()` - Create LLM fix prompt
- `apply_fixes()` - Apply or log code fixes
- `check()` - Complete check process
- `get_fix_history()` - Retrieve fix attempt history
- `save_report()` - Save check report

**Usage**:
```python
from framework.core import run_check

success, summary = run_check(
    system_path="generated_systems/my_system",
    tech_spec_path="specs/tech_spec.md",
    auto_fix=True,
    llm_client=llm
)

# Or for detailed control:
checker = CheckMechanism(
    system_path="generated_systems/my_system",
    llm_client=llm
)
success, summary = checker.check(
    tech_spec_path="specs/tech_spec.md",
    auto_fix=True
)
```

**Imports**:
- `subprocess` - Run pytest
- `pathlib.Path` - File operations
- `typing` - Type hints
- `json` - Report serialization
- `datetime` - Timestamping

### \_\_init\_\_.py

**Purpose**: Package initialization for framework.core  
**Exports**:
- `AzureLLMClient`
- `get_llm_client`
- `CheckMechanism`
- `run_check`

**Usage**:
```python
from framework.core import AzureLLMClient, get_llm_client
from framework.core import CheckMechanism, run_check
```

---

## generated_systems/

Directory where all generated systems are stored.

### [system_name]/

Each system has its own directory with standardized structure.

#### [system_name]/specs/

Specification files for the system:
- `usr_spec.md` - User system specification
- `arch_spec.md` - Architectural specification
- `tech_spec.md` - Technical specification
- `test_spec.md` - Test specification

#### [system_name]/src/

Source code directory:
- `agents/` - Agent implementations
  - `__init__.py`
  - `agent_name.py` (one per agent)
- `tools/` - Tool implementations
  - `__init__.py`
  - `tool_name.py` (one per tool)
- `utils/` - Utility modules
  - `__init__.py`
  - `config.py` - Configuration
  - `logger.py` - Logging setup
- `graph.py` - LangGraph configuration
- `main.py` - Main entry point

#### [system_name]/tests/

Test suite directory:
- `conftest.py` - Pytest fixtures and configuration
- `__init__.py`
- `unit/` - Unit tests
  - `test_agents.py`
  - `test_tools.py`
  - `test_utils.py`
- `integration/` - Integration tests
  - `test_agent_interactions.py`
  - `test_workflows.py`
- `e2e/` - End-to-end tests
  - `test_system_workflows.py`
- `fixtures/` - Test fixtures and mocks
  - `mock_data.py`
  - `mocks.py`

#### [system_name]/requirements.txt

System dependencies - generated as part of SRC generation

#### [system_name]/README.md

System-specific documentation - generated as part of SRC generation

---

## Quick Reference: File Purpose Matrix

| File | Created By | Used By | Purpose |
|------|-----------|---------|---------|
| USR_SPEC_TEMPLATE.md | User | ARCH_PROMPT | Define system requirements |
| ARCH_SPEC_TEMPLATE.md | ARCH_PROMPT | TECH_PROMPT, TEST_SPEC_PROMPT | Define system architecture |
| TECH_SPEC_TEMPLATE.md | TECH_PROMPT | CODE_PROMPT, TEST_SPEC_PROMPT | Define implementation details |
| TEST_SPEC_TEMPLATE.md | TEST_SPEC_PROMPT | TEST_CODE_PROMPT | Define test cases |
| ARCH_PROMPT.md | Framework | LLM | Generate ARCH_SPEC |
| TECH_PROMPT.md | Framework | LLM | Generate TECH_SPEC |
| CODE_PROMPT.md | Framework | LLM | Generate source code |
| TEST_SPEC_PROMPT.md | Framework | LLM | Generate TEST_SPEC |
| TEST_CODE_PROMPT.md | Framework | LLM | Generate test code |
| llm_client.py | Framework | User code | Access Azure OpenAI |
| chk.py | Framework | User code | Test and fix systems |

---

## How Files Flow Through the System

```
User Input
    ↓
USR_SPEC (user writes)
    ↓
ARCH_PROMPT + ARCH_SPEC_TMP → (LLM) → ARCH_SPEC
    ↓
TECH_PROMPT + TECH_SPEC_TMP → (LLM) → TECH_SPEC
    ↓
┌─────────────────────────┐
│  CODE_PROMPT → (LLM) → SRC (Source Code)
│  TEST_SPEC_PROMPT → (LLM) → TEST_SPEC
└─────────────────────────┘
    ↓
TEST_CODE_PROMPT + TEST_SPEC → (LLM) → TST (Test Code)
    ↓
CHK (llm_client.py + chk.py)
    ├→ Run tests (pytest)
    ├→ If fail: generate fixes
    ├→ Rerun tests
    └→ Report results
    ↓
✓ System Ready
```

---

## Summary

The framework provides:

1. **Templates** (specifications/): Structure for defining systems at multiple levels
2. **Prompts** (prompts/): Instructions for LLM to generate each artifact
3. **Core Utilities** (core/): Python tools for LLM access and testing
4. **Documentation**: Guides, examples, and workflows
5. **Generated Systems** (generated_systems/): Output directory for created systems

Each component serves a specific purpose in the workflow from requirements to working system.
