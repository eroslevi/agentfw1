# Quick Start Guide

This guide will help you get started with the Intelligent Multi-Agentic System Framework.

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd agentfw1
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI
```bash
# Set environment variables
export AZURE_OPENAI_ENDPOINT="https://your-instance.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-api-key-here"
```

### 3. Verify Installation
```bash
python -c "from framework.core import get_llm_client; print('✓ Framework ready!')"
```

## Creating Your First System

### Step 1: Define System Goals (5 min)

Create `my_system_spec.md`:
```markdown
# My Intelligent System

## Project Title
Task Automation System

## Primary Goals
- Automate routine tasks
- Process user requests
- Provide intelligent responses

## Key Requirements
- Fast response time (< 2 seconds)
- Support 10+ concurrent users
- 99% uptime

## Input Data
- User text queries
- System state information

## Expected Output
- Task execution result
- Status updates
- Error messages

## Success Criteria
- All tasks complete successfully
- Response within time limits
- User satisfaction > 80%
```

### Step 2: Generate Architecture (2 min)

```python
from framework.core import get_llm_client
from pathlib import Path

# Initialize LLM
llm = get_llm_client()

# Read your system specification
with open("my_system_spec.md") as f:
    usr_spec = f.read()

# Read the architecture prompt
with open("framework/prompts/ARCH_PROMPT.md") as f:
    arch_prompt = f.read()

# Generate architecture
print("Generating architectural specification...")
arch_spec = llm.generate_specification(
    template=arch_prompt,
    context=usr_spec,
    spec_type="architectural specification",
    max_tokens=4000
)

# Save it
with open("my_arch_spec.md", "w") as f:
    f.write(arch_spec)

print("✓ Architecture saved to my_arch_spec.md")
```

### Step 3: Generate Technical Spec (2 min)

```python
# Read the architecture we just created
with open("my_arch_spec.md") as f:
    arch_spec = f.read()

# Read the technical prompt
with open("framework/prompts/TECH_PROMPT.md") as f:
    tech_prompt = f.read()

# Generate technical specification
print("Generating technical specification...")
tech_spec = llm.generate_specification(
    template=tech_prompt,
    context=arch_spec,
    spec_type="technical specification",
    max_tokens=4000
)

# Save it
with open("my_tech_spec.md", "w") as f:
    f.write(tech_spec)

print("✓ Technical spec saved to my_tech_spec.md")
```

### Step 4: Generate Source Code (3 min)

```python
# Read the technical specification
with open("my_tech_spec.md") as f:
    tech_spec = f.read()

# Read the code generation prompt
with open("framework/prompts/CODE_PROMPT.md") as f:
    code_prompt = f.read()

# Generate source code
print("Generating source code...")
src_code = llm.generate_from_prompt(
    system_prompt=code_prompt,
    user_prompt=tech_spec,
    max_tokens=4000
)

# Create system directory
system_dir = Path("generated_systems/my_system")
system_dir.mkdir(parents=True, exist_ok=True)
(system_dir / "src").mkdir(exist_ok=True)

# Save source code (you may need to parse and organize files)
with open(system_dir / "src" / "main.py", "w") as f:
    f.write(src_code[:2000])  # Initial part

print(f"✓ Source code generated in {system_dir}")
```

### Step 5: Generate Tests (2 min)

```python
# Read specifications
with open("my_arch_spec.md") as f:
    arch_spec = f.read()

with open("my_tech_spec.md") as f:
    tech_spec = f.read()

# Generate test specification
with open("framework/prompts/TEST_SPEC_PROMPT.md") as f:
    test_spec_prompt = f.read()

combined = f"{arch_spec}\n\n{tech_spec}"

print("Generating test specification...")
test_spec = llm.generate_specification(
    template=test_spec_prompt,
    context=combined,
    spec_type="test specification",
    max_tokens=4000
)

with open("my_test_spec.md", "w") as f:
    f.write(test_spec)

print("✓ Test spec saved to my_test_spec.md")
```

### Step 6: Run Tests and Check

```python
from framework.core import run_check

# Make sure you've generated the code in the proper structure first
success, summary = run_check(
    system_path="generated_systems/my_system",
    tech_spec_path="my_tech_spec.md",
    auto_fix=False,  # Set to True for automatic fixes
    llm_client=llm
)

print(f"\nCheck Result:\n{summary}")

if success:
    print("✓ Your system is ready!")
else:
    print("Review the failures above and update your code")
```

## File Organization

After following the steps above, your structure will be:

```
agentfw1/
├── framework/
│   ├── specifications/     # Templates
│   ├── prompts/           # Generation prompts
│   └── core/              # Core utilities
├── generated_systems/
│   └── my_system/
│       ├── src/           # Your generated source code
│       ├── tests/         # Your test files
│       ├── specs/         # Your specification files
│       └── requirements.txt
├── my_system_spec.md      # Your user specification
├── my_arch_spec.md        # Generated architecture
├── my_tech_spec.md        # Generated technical spec
├── my_test_spec.md        # Generated test spec
└── README.md
```

## Common Patterns

### Pattern 1: Multi-Agent System

In your USR_SPEC, specify multiple agents:
```markdown
## Key Requirements
- Agent 1: Document processor
- Agent 2: Data analyzer
- Agent 3: Report generator
```

ARCH_PROMPT will define agent responsibilities and interactions.

### Pattern 2: Tool Integration

Specify external tools in requirements:
```markdown
## Key Requirements
- Use API: https://api.example.com
- Database: PostgreSQL
- Cache: Redis
```

ARCH_PROMPT will design tool interfaces.

### Pattern 3: Error Handling

Be specific about error scenarios:
```markdown
## Constraints and Limitations
- Handle network timeouts gracefully
- Retry failed API calls up to 3 times
- Log all errors for debugging
```

TECH_SPEC will include error handling in method signatures.

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"

```bash
pip install openai>=1.0.0
```

### "AZURE_OPENAI_ENDPOINT environment variable not found"

```bash
# Option 1: Set environment variable
export AZURE_OPENAI_ENDPOINT="https://your-instance.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-api-key"

# Option 2: Pass to function
llm = get_llm_client(
    azure_endpoint="https://...",
    api_key="key..."
)
```

### Generated code seems incomplete

This can happen if max_tokens is too low. Try:
```python
spec = llm.generate_specification(
    template=prompt,
    context=context,
    spec_type="...",
    max_tokens=8000  # Increase from default
)
```

### Tests are failing

1. Review the error messages in test output
2. Check your USR_SPEC and ARCH_SPEC for clarity
3. Manually review generated code
4. Run with `auto_fix=False` first to understand issues

## Next Steps

1. Read the main [README.md](README.md) for detailed documentation
2. Review template files in `framework/specifications/`
3. Examine prompt files in `framework/prompts/`
4. Explore the API in `framework/core/`
5. Build your first intelligent system!

## Tips for Success

- **Start small**: Begin with a simple single-agent system
- **Be specific**: Write detailed, clear requirements in USR_SPEC
- **Review specs**: Don't skip reviewing generated specifications
- **Iterate**: Use CHK frequently to validate your system
- **Document**: Add comments and documentation to generated code
- **Test incrementally**: Add tests as you build features

---

Happy building! 🚀
