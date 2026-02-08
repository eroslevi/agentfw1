# Intelligent Multi-Agentic System Framework

A comprehensive framework for generating intelligent multi-agentic systems powered by LangGraph and Azure OpenAI. This framework provides templates, prompts, and tools for creating, testing, and refining agentic systems through a structured specification-driven approach.

## Table of Contents

- [Overview](#overview)
- [Framework Components](#framework-components)
- [Getting Started](#getting-started)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Key Files and Templates](#key-files-and-templates)
- [System Generation Process](#system-generation-process)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

The framework enables you to systematically define, design, implement, test, and refine multi-agentic systems using a specification-driven approach. It leverages Azure-hosted OpenAI models to assist in generating specifications and code, ensuring consistency and quality throughout the development lifecycle.

### Key Features

- **Specification-Driven Development:** Define systems through structured specifications at multiple levels
- **Multi-Step Generation Pipeline:** User specifications → Architectural specs → Technical specs → Source code
- **Comprehensive Testing:** Specification-driven test generation and validation
- **Automated Code Fixing:** Optional automatic code fixes based on test failures
- **LangGraph Integration:** First-class support for LangGraph-based agentic systems
- **Azure OpenAI Integration:** Use your own Azure OpenAI instance for specification generation

## Framework Components

### 1. Specifications Directory (`framework/specifications/`)

Contains templates and generated specifications:

- **USR_SPEC_TEMPLATE.md** - Template for user system specifications
  - Project goals and requirements
  - Input/output specifications
  - Success criteria and constraints

- **ARCH_SPEC_TEMPLATE.md** - Template for architectural specifications
  - Agent definitions and interactions
  - Tool definitions and interactions
  - Data flow and integration points

- **TECH_SPEC_TEMPLATE.md** - Template for technical specifications
  - Python method signatures for agents
  - Python method signatures for tools
  - Utility functions and configuration

- **TEST_SPEC_TEMPLATE.md** - Template for test specifications
  - Unit test cases
  - Integration test cases
  - E2E test cases and performance criteria

### 2. Prompts Directory (`framework/prompts/`)

Contains LLM prompts for generation:

- **ARCH_PROMPT.md** - Generates ARCH_SPEC from USR_SPEC
- **TECH_PROMPT.md** - Generates TECH_SPEC from ARCH_SPEC
- **CODE_PROMPT.md** - Generates source code from TECH_SPEC
- **TEST_SPEC_PROMPT.md** - Generates TEST_SPEC from ARCH_SPEC + TECH_SPEC
- **TEST_CODE_PROMPT.md** - Generates test code from TEST_SPEC

### 3. Core Module (`framework/core/`)

Framework utilities:

- **llm_client.py** - Azure OpenAI LLM access interface
- **chk.py** - Test runner and automatic code fixing mechanism

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda package manager
- Azure OpenAI instance (URI and API key)
- Git (optional, for version control)

### Installation

1. Clone or navigate to the framework directory:
```bash
cd agentfw1
```

2. Install framework dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `openai` - Azure OpenAI SDK
- `langgraph` - Multi-agent orchestration
- `langchain` - LLM framework
- `pytest` - Testing framework
- `pytest-mock` - Mocking support for tests

3. Set up Azure OpenAI credentials:
```bash
# Option 1: Environment variables
export AZURE_OPENAI_ENDPOINT="https://your-instance.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-api-key-here"

# Option 2: Create .env file in framework/core/
echo "AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/" > .env
echo "AZURE_OPENAI_API_KEY=your-api-key-here" >> .env
```

## Workflow

The framework follows a structured, multi-step workflow:

### Step 1: Define User Specifications (USR_SPEC)

Create a detailed user specification describing what your system should do:

```markdown
# Example: Document Analysis System USR_SPEC

## Project Title
Multi-Document Analysis Agent System

## Primary Goals
- Analyze documents for key information
- Extract structured data from unstructured content
- Generate summaries

## Key Requirements
- Support PDF, DOC, TXT formats
- Process documents concurrently
- Return analysis within 30 seconds
```

Use the template: `framework/specifications/USR_SPEC_TEMPLATE.md`

### Step 2: Generate Architectural Specification (ARCH_SPEC)

Use the ARCH_PROMPT with your USR_SPEC to generate the architectural specification:

```python
from framework.core.llm_client import get_llm_client

# Initialize LLM client
llm = get_llm_client()

# Read your USR_SPEC
with open("my_usr_spec.md") as f:
    usr_spec = f.read()

# Read the prompts and template
with open("framework/prompts/ARCH_PROMPT.md") as f:
    arch_prompt = f.read()

# Generate ARCH_SPEC
arch_spec = llm.generate_specification(
    template=arch_prompt,
    context=usr_spec,
    spec_type="architectural specification"
)

# Save the generated ARCH_SPEC
with open("my_arch_spec.md", "w") as f:
    f.write(arch_spec)
```

The resulting ARCH_SPEC includes:
- Agent definitions and responsibilities
- Tool specifications and functionality
- Data flow architecture
- Integration points

### Step 3: Generate Technical Specification (TECH_SPEC)

Use TECH_PROMPT with ARCH_SPEC to generate detailed technical specifications:

```python
# Read ARCH_SPEC
with open("my_arch_spec.md") as f:
    arch_spec = f.read()

# Generate TECH_SPEC
tech_spec = llm.generate_specification(
    template=open("framework/prompts/TECH_PROMPT.md").read(),
    context=arch_spec,
    spec_type="technical specification"
)

# Save TECH_SPEC
with open("my_tech_spec.md", "w") as f:
    f.write(tech_spec)
```

TECH_SPEC includes:
- Exact Python class definitions
- Method signatures with type hints
- Implementation details
- LangGraph node configuration

### Step 4: Generate Test Specification (TEST_SPEC)

Generate comprehensive test specifications from ARCH_SPEC + TECH_SPEC:

```python
# Combine ARCH and TECH specs
combined_context = f"""
## Architectural Context:
{arch_spec}

## Technical Context:
{tech_spec}
"""

# Generate TEST_SPEC
test_spec = llm.generate_specification(
    template=open("framework/prompts/TEST_SPEC_PROMPT.md").read(),
    context=combined_context,
    spec_type="test specification"
)

with open("my_test_spec.md", "w") as f:
    f.write(test_spec)
```

### Step 5: Generate Source Code (SRC)

Generate the main system source code:

```python
# Generate source code
src_code = llm.generate_from_prompt(
    system_prompt=open("framework/prompts/CODE_PROMPT.md").read(),
    user_prompt=tech_spec
)

# Save to generated_systems/[system_name]/src/
system_dir = Path("generated_systems/my_system")
system_dir.mkdir(parents=True, exist_ok=True)
(system_dir / "src").mkdir(exist_ok=True)

# Parse and save individual files from generated code
# The CODE_PROMPT should output code organized by file
```

### Step 6: Generate Test Code (TST)

Generate test suite code:

```python
# Generate test code
test_code = llm.generate_from_prompt(
    system_prompt=open("framework/prompts/TEST_CODE_PROMPT.md").read(),
    user_prompt=test_spec
)

# Save to generated_systems/[system_name]/tests/
test_dir = Path("generated_systems/my_system/tests")
test_dir.mkdir(parents=True, exist_ok=True)

# Save test files
```

### Step 7: Run Check (CHK) - Test and Fix

Execute the check mechanism to run tests and optionally fix failures:

```python
from framework.core.chk import run_check

# Run tests and attempt auto-fixes if needed
success, summary = run_check(
    system_path="generated_systems/my_system",
    tech_spec_path="my_tech_spec.md",
    auto_fix=True,
    llm_client=llm
)

print(f"Check Result: {summary}")
```

The CHK mechanism:
1. **Runs the test suite** - Executes all tests with pytest
2. **Checks results:**
   - If all pass → Success, returns
   - If any fail → Collects failure info
3. **Generates fixes** - Uses LLM to suggest code fixes (if auto_fix=True)
4. **Applies fixes** - Logs suggestions for manual or automatic application
5. **Reruns tests** - Verifies fixes work
6. **Reports** - Provides summary and detailed report

## Project Structure

```
agentfw1/
├── framework/
│   ├── specifications/
│   │   ├── USR_SPEC_TEMPLATE.md
│   │   ├── ARCH_SPEC_TEMPLATE.md
│   │   ├── TECH_SPEC_TEMPLATE.md
│   │   └── TEST_SPEC_TEMPLATE.md
│   ├── prompts/
│   │   ├── ARCH_PROMPT.md
│   │   ├── TECH_PROMPT.md
│   │   ├── CODE_PROMPT.md
│   │   ├── TEST_SPEC_PROMPT.md
│   │   └── TEST_CODE_PROMPT.md
│   └── core/
│       ├── llm_client.py
│       ├── chk.py
│       └── __init__.py
├── generated_systems/
│   └── [system_name]/
│       ├── specs/
│       │   ├── usr_spec.md
│       │   ├── arch_spec.md
│       │   ├── tech_spec.md
│       │   └── test_spec.md
│       ├── src/
│       │   ├── agents/
│       │   ├── tools/
│       │   ├── utils/
│       │   ├── graph.py
│       │   └── main.py
│       ├── tests/
│       │   ├── unit/
│       │   ├── integration/
│       │   ├── e2e/
│       │   └── conftest.py
│       ├── requirements.txt
│       └── README.md
└── README.md (this file)
```

## Key Files and Templates

### USR_SPEC_TEMPLATE.md

The starting point where you define what the system should do:

```markdown
# User System Specification

## Project Title
[Your system name]

## Project Description
[What it does]

## Primary Goals
- Goal 1
- Goal 2

## Key Requirements
- Requirement 1
- Requirement 2

## Success Criteria
- Criteria 1
- Criteria 2
```

### ARCH_SPEC_TEMPLATE.md

Defines system architecture with agents and tools:

```markdown
# Architectural Specification

## Agents

### Agent: DocumentAnalyzer
**Functionality:** Analyzes documents for key information
**Interactions:** Works with DataExtractor and Summarizer agents

## Tools

### Tool: PDFParser
**Functionality:** Extracts text from PDF files
**Input Parameters:** file_path (str), options (dict)
```

### TECH_SPEC_TEMPLATE.md

Specifies Python implementations:

```markdown
# Technical Specification

## Agent Implementation

### Agent: DocumentAnalyzer
**Class:** DocumentAnalyzer
**Module:** agents/document_analyzer.py

#### Method: analyze
- **Signature:** def analyze(self, document: Document) -> Analysis:
- **Parameters:** document - Document object to analyze
- **Return:** Analysis object with results
```

### TEST_SPEC_TEMPLATE.md

Defines test cases:

```markdown
# Test Specification

## Test Case: Analyze Simple Document

**Test ID:** TC_001
**Type:** Unit Test
**Component:** DocumentAnalyzer.analyze()

**Steps:**
1. Create sample document
2. Call analyze()
3. Verify results

**Assertions:**
- Assert result is not None
- Assert result.summary is not empty
```

## System Generation Process

### Complete Workflow Example

```python
from pathlib import Path
from framework.core.llm_client import get_llm_client
from framework.core.chk import run_check

# Initialize
llm = get_llm_client()
system_name = "document_analyzer"
system_dir = Path(f"generated_systems/{system_name}")

# 1. Define user specification
usr_spec = """
# Document Analysis System

## Goals
- Analyze documents
- Extract key information
- Generate summaries

## Requirements
- Process PDFs, DOC files
- Return results in JSON format
"""

# 2. Generate ARCH_SPEC
print("Generating architectural specification...")
arch_spec = llm.generate_specification(
    template=open("framework/prompts/ARCH_PROMPT.md").read(),
    context=usr_spec,
    spec_type="architectural"
)

# 3. Generate TECH_SPEC
print("Generating technical specification...")
tech_spec = llm.generate_specification(
    template=open("framework/prompts/TECH_PROMPT.md").read(),
    context=arch_spec,
    spec_type="technical"
)

# 4. Generate source code
print("Generating source code...")
src_code = llm.generate_from_prompt(
    system_prompt=open("framework/prompts/CODE_PROMPT.md").read(),
    user_prompt=tech_spec
)

# 5. Generate test specification
print("Generating test specification...")
test_spec = llm.generate_specification(
    template=open("framework/prompts/TEST_SPEC_PROMPT.md").read(),
    context=f"{arch_spec}\n{tech_spec}",
    spec_type="test"
)

# 6. Generate test code
print("Generating test code...")
test_code = llm.generate_from_prompt(
    system_prompt=open("framework/prompts/TEST_CODE_PROMPT.md").read(),
    user_prompt=test_spec
)

# 7. Run tests and fix issues
print("Running tests and checking for issues...")
success, summary = run_check(
    system_path=str(system_dir),
    tech_spec_path=str(system_dir / "specs" / "tech_spec.md"),
    auto_fix=True,
    llm_client=llm
)

print(f"\nFinal Result: {summary}")
if success:
    print(f"✓ System {system_name} is ready for deployment!")
else:
    print(f"✗ System {system_name} requires manual fixes")
```

## API Reference

### LLM Client

#### `AzureLLMClient`

Main interface for Azure OpenAI LLM access.

```python
from framework.core.llm_client import AzureLLMClient

# Initialize
client = AzureLLMClient(
    azure_endpoint="https://your-instance.openai.azure.com/",
    api_key="your-api-key",
    api_version="2024-02-15-preview",
    deployment_name="gpt-4"
)

# Generate text
response = client.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "What is?"}
    ],
    temperature=0.7,
    max_tokens=1000
)

# Generate with retries
response = client.create_chat_completion_with_retries(
    messages=messages,
    max_retries=3,
    retry_delay=1.0
)

# Generate from prompts
response = client.generate_from_prompt(
    system_prompt="You are an architect",
    user_prompt="Design a system for...",
    temperature=0.5
)

# Generate specification
spec = client.generate_specification(
    template=template_content,
    context="Requirements: ...",
    spec_type="technical"
)
```

### Check Mechanism

#### `CheckMechanism`

Test runner and code fixing orchestrator.

```python
from framework.core.chk import CheckMechanism, run_check

# Detailed usage
checker = CheckMechanism(
    system_path="generated_systems/my_system",
    test_dir="tests",
    src_dir="src",
    max_fix_attempts=3,
    llm_client=llm_client
)

# Run tests
all_passed, output = checker.run_tests(verbose=True)

# Run full check process
success, summary = checker.check(
    tech_spec_path="specs/tech_spec.md",
    auto_fix=True
)

# Get fix history
history = checker.get_fix_history()

# Save report
checker.save_report("check_report.json")

# Or use convenience function
success, summary = run_check(
    system_path="generated_systems/my_system",
    tech_spec_path="specs/tech_spec.md",
    auto_fix=True,
    llm_client=llm_client
)
```

## Examples

### Example 1: Simple Agent System

Create a system with a single agent that processes information:

1. **Create USR_SPEC** with your system goals
2. **Use ARCH_PROMPT** to generate agent and tool design
3. **Use TECH_PROMPT** to get exact method signatures
4. **Use CODE_PROMPT** to generate agent class
5. **Use TEST_SPEC_PROMPT** to get test cases
6. **Use TEST_CODE_PROMPT** to generate pytest tests
7. **Run CHK** to verify and fix

### Example 2: Multi-Agent Coordination

For a system with multiple agents:

1. Define multiple agents in USR_SPEC requirements
2. ARCH_SPEC will detail agent-to-agent communication
3. TECH_SPEC will specify all methods for coordination
4. Generated code will implement LangGraph routing
5. Tests will verify agent handoffs and data flow

### Example 3: Tool Integration

To add external tools (APIs, databases):

1. Specify tools in USR_SPEC requirements
2. ARCH_SPEC defines tool interfaces
3. TECH_SPEC details tool method signatures
4. CODE_PROMPT generates tool classes
5. TEST_SPEC_PROMPT ensures tool integration is tested

## Troubleshooting

### Issue: Azure credentials not found

**Solution:**
```bash
# Set environment variables
export AZURE_OPENAI_ENDPOINT="https://your-instance.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-api-key"

# Or create .env file
# and use python-dotenv to load it
```

### Issue: Tests fail with "module not found"

**Solution:**
```bash
# Ensure all dependencies are installed
cd generated_systems/[system_name]
pip install -r requirements.txt

# Run from the system directory
cd /path/to/system
pytest tests/
```

### Issue: LLM generation produces incomplete code

**Solution:**
- Break specifications into smaller, more focused sections
- Provide more detailed context in prompts
- Use smaller max_tokens initially and iterate
- Review and edit generated code manually if needed

### Issue: Tests still fail after auto-fix attempts

**Solution:**
1. Review the generated code for logical errors
2. Check if specifications match implementation
3. Manually edit source code and rerun CHK
4. Review test expectations in TEST_SPEC

## Best Practices

1. **Write detailed USR_SPEC** - The clearer your requirements, the better the generated system
2. **Review generated ARCH_SPEC** - Ensure architecture matches your vision before proceeding
3. **Validate TECH_SPEC** - Review method signatures to ensure they match your design
4. **Use meaningful test cases** - Good tests catch issues early
5. **Iterate and refine** - Use CHK to validate and improve incrementally
6. **Version control** - Keep specifications and generated code in Git
7. **Document manually** - Generated code will have docstrings, but add additional documentation

## Contributing

To extend the framework:

1. Add new prompt templates in `framework/prompts/`
2. Extend `AzureLLMClient` for additional LLM features
3. Enhance `CheckMechanism` for better code analysis
4. Add new specification templates as needed

## License

This framework is provided as-is for generating intelligent multi-agentic systems.

## Support

For issues or questions:
1. Review the examples and documentation above
2. Check troubleshooting section
3. Review generated code against templates
4. Validate specifications with domain experts

---

**Framework Version:** 1.0  
**Last Updated:** February 8, 2026  
**Python Requirement:** 3.8+
