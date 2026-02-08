# Framework Workflow

This document describes the complete workflow for using the Intelligent Multi-Agentic System Framework.

## High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USER DEFINES SYSTEM REQUIREMENTS                            │
│     Create USR_SPEC with goals, requirements, I/O specs        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. GENERATE ARCHITECTURE (ARCH_PROMPT)                         │
│     Input: USR_SPEC + ARCH_SPEC_TMP                            │
│     Output: ARCH_SPEC (Agent & Tool design)                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼ (Review & Refine if needed)
                           │
┌─────────────────────────────────────────────────────────────────┐
│  3. GENERATE TECHNICAL SPEC (TECH_PROMPT)                       │
│     Input: ARCH_SPEC + TECH_SPEC_TMP                          │
│     Output: TECH_SPEC (Python methods & signatures)            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼ (Review & Refine if needed)
                           │
┌─────────────────────────────────────────────────────────────────┐
│  4. GENERATE SOURCE CODE (CODE_PROMPT)                          │
│     Input: TECH_SPEC + CODE_PROMPT                            │
│     Output: SRC (Production-ready Python code)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  │                  │
┌──────────────────┐       │                  │
│ Save Source Code │       │                  │
│ to src/          │       │                  │
└──────────────────┘       │                  │
                           │                  │
                           ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. GENERATE TEST SPEC & CODE                                   │
│     Path 1: TEST_SPEC_PROMPT → TEST_SPEC                       │
│     Path 2: TEST_CODE_PROMPT → TST (test suite code)          │
│     Input: ARCH_SPEC + TECH_SPEC (for TEST_SPEC_PROMPT)       │
│     Input: TEST_SPEC (for TEST_CODE_PROMPT)                   │
│     Output: TST (pytest test files)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. SAVE AND ORGANIZE                                           │
│     Directory structure:                                         │
│     generated_systems/[system_name]/                            │
│       ├── src/          (SRC - source code)                     │
│       ├── tests/        (TST - test code)                       │
│       ├── specs/        (ARCH_SPEC, TECH_SPEC, TEST_SPEC)     │
│       └── requirements.txt                                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  7. RUN CHECK (CHK)                                              │
│     Execute: python -m pytest tests/                            │
│     ┌─ If all pass → ✓ System ready                            │
│     └─ If any fail → Continue to step 8                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    (if auto_fix=True)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  8. AUTO-FIX FAILURES (Optional)                                │
│     For each test failure:                                      │
│     1. Parse test output                                        │
│     2. Use LLM to generate fixes                               │
│     3. Log suggestions (can be auto-applied)                   │
│     4. Rerun tests                                             │
│     5. Repeat up to max_fix_attempts                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  9. FINAL RESULT                                                │
│     ✓ All tests pass → System ready for deployment             │
│     ✗ Tests still fail → Manual fixes required                 │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Process Flow

### Phase 1: Requirements Definition

**User Creates USR_SPEC**

File: `my_system_spec.md`

```markdown
# Project Title
My Intelligent System

# Primary Goals
- Goal 1
- Goal 2

# Key Requirements
- Requirement 1
- Requirement 2

# Success Criteria
- Can be measured
- Objective and clear
```

**Purpose**: Clearly document what the system should do without prescribing how

### Phase 2: Architecture Design

**ARCH_PROMPT + USR_SPEC → ARCH_SPEC**

```python
# Pseudo-code
arch_spec = llm.generate_specification(
    template=ARCH_SPEC_TMP,
    context=USR_SPEC,
    spec_type="architectural"
)
```

**ARCH_SPEC Contains**:
- Agents: Name, responsibility, interactions
- Tools: Name, functionality, parameters
- Data flows: How information moves through system
- Integration points: External services

**File**: `my_arch_spec.md`

### Phase 3: Technical Design

**TECH_PROMPT + ARCH_SPEC → TECH_SPEC**

```python
tech_spec = llm.generate_specification(
    template=TECH_SPEC_TMP,
    context=ARCH_SPEC,
    spec_type="technical"
)
```

**TECH_SPEC Contains**:
- Python class definitions
- Method signatures with type hints
- Parameter descriptions
- Return type specifications
- Implementation notes

**File**: `my_tech_spec.md`

### Phase 4: Code Generation

**CODE_PROMPT + TECH_SPEC → SRC**

```python
src_code = llm.generate_from_prompt(
    system_prompt=CODE_PROMPT,
    user_prompt=TECH_SPEC
)
```

**SRC Directory Structure**:
```
src/
├── agents/
│   ├── __init__.py
│   ├── agent1.py
│   └── agent2.py
├── tools/
│   ├── __init__.py
│   ├── tool1.py
│   └── tool2.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   └── logger.py
├── graph.py
└── main.py
```

### Phase 5: Test Design

**TEST_SPEC_PROMPT + ARCH_SPEC + TECH_SPEC → TEST_SPEC**

```python
test_spec = llm.generate_specification(
    template=TEST_SPEC_TMP,
    context=f"{ARCH_SPEC}\n{TECH_SPEC}",
    spec_type="test"
)
```

**TEST_SPEC Contains**:
- Unit test cases
- Integration test cases
- E2E test cases
- Performance criteria
- Edge case coverage

**File**: `my_test_spec.md`

### Phase 6: Test Code Generation

**TEST_CODE_PROMPT + TEST_SPEC → TST**

```python
test_code = llm.generate_from_prompt(
    system_prompt=TEST_CODE_PROMPT,
    user_prompt=TEST_SPEC
)
```

**TST Directory Structure**:
```
tests/
├── conftest.py
├── __init__.py
├── unit/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_utils.py
├── integration/
│   ├── test_agent_interactions.py
│   └── test_workflows.py
├── e2e/
│   └── test_system_workflows.py
└── fixtures/
    ├── mock_data.py
    └── mocks.py
```

### Phase 7: Testing and Validation (CHK)

**CHK Process**

```python
success, summary = run_check(
    system_path="generated_systems/my_system",
    tech_spec_path="my_tech_spec.md",
    auto_fix=True,  # Optional automatic fixing
    llm_client=llm
)
```

**CHK Steps**:

1. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

2. **Analyze Results**
   - If ✓ all pass → Success, return
   - If ✗ some fail → Continue

3. **Parse Failures**
   - Extract error messages
   - Identify failing test cases
   - Determine root causes

4. **Generate Fixes** (if auto_fix=True)
   - Create fix prompt with failure context
   - Request LLM suggestions
   - Log suggested changes

5. **Apply Fixes** (manual or automatic)
   - Modify source code based on suggestions
   - Or log for manual application

6. **Rerun Tests**
   - Execute test suite again
   - Repeat up to max_fix_attempts (default: 3)

7. **Report Results**
   - Success if all tests pass
   - Failure with details if max attempts reached

## Decision Points

```
Does USR_SPEC need revision?
├─ Yes → Revise USR_SPEC, restart workflow
└─ No → Proceed to ARCH_PROMPT

Does ARCH_SPEC look correct?
├─ No → Revise, run ARCH_PROMPT again
└─ Yes → Proceed to TECH_PROMPT

Does TECH_SPEC have correct methods?
├─ No → Revise, run TECH_PROMPT again
└─ Yes → Proceed to CODE_PROMPT

Do tests pass with generated code?
├─ No & auto_fix=True → Auto-fix attempts
├─ No & auto_fix=False → Manual fixes
└─ Yes → System is ready!
```

## Feedback Loops

The framework supports multiple feedback loops:

### Loop 1: Specification Refinement
If generated code doesn't match expectations:
1. Review ARCH_SPEC
2. Refine it if needed
3. Regenerate TECH_SPEC
4. Regenerate code

### Loop 2: Test-Driven Fixes
If tests fail:
1. CHK analyzes failures
2. LLM suggests fixes
3. Developer applies fixes
4. CHK reruns tests
5. Repeat until passing (max 3 attempts)

### Loop 3: Manual Improvement
If auto-fixes aren't working:
1. Review test output and source code
2. Make manual corrections
3. Run CHK again
4. Verify fixes

## Example Timeline

For a typical system:

| Phase | Time | Tool |
|-------|------|------|
| 1. Create USR_SPEC | 20 min | Text editor |
| 2. Generate ARCH_SPEC | 2 min | ARCH_PROMPT |
| 3. Review/refine ARCH_SPEC | 10 min | Text editor |
| 4. Generate TECH_SPEC | 2 min | TECH_PROMPT |
| 5. Review/refine TECH_SPEC | 10 min | Text editor |
| 6. Generate SRC | 2 min | CODE_PROMPT |
| 7. Save and organize | 5 min | File system |
| 8. Generate TEST_SPEC | 2 min | TEST_SPEC_PROMPT |
| 9. Generate TST | 2 min | TEST_CODE_PROMPT |
| 10. Run CHK | 1 min | CHK |
| 11. Fix issues (if needed) | 10-30 min | Manual + CHK |
| **Total** | **~60-90 min** | |

## Best Practices

1. **Start with clear USR_SPEC**: The better your requirements, the better your system
2. **Review each generated spec**: Don't skip specifications, validate they make sense
3. **Run CHK frequently**: Catch issues early in the development cycle
4. **Keep specifications DRY**: Avoid redundancy across specs
5. **Document manually**: Add extra documentation to generated code
6. **Use version control**: Track specifications and code changes
7. **Iterate incrementally**: Don't try to build everything at once

## Conclusion

This workflow ensures:
- ✓ Clear requirements (USR_SPEC)
- ✓ Sound architecture (ARCH_SPEC)
- ✓ Precise implementation plan (TECH_SPEC)
- ✓ Correct implementation (SRC)
- ✓ Comprehensive testing (TST)
- ✓ Working system (CHK validation)

Each phase builds on the previous, with clear inputs and outputs, enabling both automation and human oversight.
