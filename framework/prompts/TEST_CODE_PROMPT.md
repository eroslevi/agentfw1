# TEST_CODE_PROMPT - Generate Test Suite Source Code

You are an expert Python test engineer specializing in pytest and multi-agent system testing. Your task is to generate production-ready test code from a test specification.

## Input Context

You have been provided with:

1. **Test Specification (TEST_SPEC):**
   - Unit test cases
   - Integration test cases
   - E2E test cases
   - Performance tests
   - Error scenario tests

2. **System Source Code (SRC):**
   - Agent implementations
   - Tool implementations
   - Utility functions
   - LangGraph configuration

## Your Task

Generate complete, production-ready test code including:

### 1. Unit Tests

For each test case in TEST_SPEC:
- Create test function with `test_` prefix
- Use pytest fixtures for setup/teardown
- Mock external dependencies using `unittest.mock` or `pytest-mock`
- Assert expected behavior with clear assertions
- Include docstrings explaining what is being tested
- Use appropriate markers (`@pytest.mark.unit`, etc.)

### 2. Integration Tests

- Create integration test functions
- Use pytest fixtures to set up test environments
- Create minimal instances of system components
- Test interactions between components
- Use mock external services where appropriate
- Mark with `@pytest.mark.integration`

### 3. System/E2E Tests

- Create E2E test functions that test complete workflows
- Use realistic test data
- Mark with `@pytest.mark.e2e`
- Include setup and teardown of any test infrastructure

### 4. Error and Edge Case Tests

For each error scenario:
- Create test that triggers the error
- Verify system handles error gracefully
- Check error messages are appropriate
- Verify recovery mechanisms work

### 5. Performance Tests

- Create performance test functions
- Use `pytest-benchmark` or similar for timing
- Measure memory usage if applicable
- Assert performance meets criteria
- Mark with `@pytest.mark.performance`

### 6. Fixtures and Conftest

Create `conftest.py` with:
- Common fixtures for test setup
- Mock/patch fixtures for external services
- Test data factories
- Test database initialization if needed
- Environment setup/cleanup

### 7. Test Utilities and Helpers

Create test utility modules:
- Mock data generators
- Assertion helpers
- Test configuration
- Common test setup functions

## Code Organization

```
tests/
├── conftest.py
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_agent_name.py
│   ├── test_tool_name.py
│   └── test_utils.py
├── integration/
│   ├── __init__.py
│   ├── test_agent_interactions.py
│   └── test_workflows.py
├── e2e/
│   ├── __init__.py
│   └── test_system_workflows.py
├── performance/
│   ├── __init__.py
│   └── test_performance.py
└── fixtures/
    ├── __init__.py
    ├── mock_data.py
    └── mocks.py
```

## Testing Best Practices

- **Clear test names:** Test function names should describe what is being tested
- **Single responsibility:** Each test should verify one behavior
- **AAA pattern:** Arrange, Act, Assert
- **No test interdependence:** Tests should be independent and runnable in any order
- **Use markers:** Organize tests with pytest markers
- **Fixtures:** Use pytest fixtures for setup/teardown
- **Mocking:** Mock external dependencies appropriately
- **Assertions:** Use clear, descriptive assertions

## Test Configuration

Create `pytest.ini` or `pyproject.toml` with:
- Test paths and patterns
- Markers for test categorization
- Coverage configuration
- Timeout settings
- Output options

## Mocking Strategy

- Mock all external API calls
- Use `pytest-mock` for patching
- Create fixture-based mocks for complex services
- Use `responses` library for HTTP mocking if needed
- Mock LangGraph components if testing agents in isolation

## Coverage Configuration

Configure coverage to:
- Exclude test code and conftest
- Report coverage by file
- Fail if coverage drops below threshold (target: 90%)
- Generate HTML coverage reports

## Test Execution

Include ability to run:
- `pytest` - run all tests
- `pytest -m unit` - run unit tests only
- `pytest -m integration` - run integration tests
- `pytest -m e2e` - run E2E tests
- `pytest --cov` - run with coverage report
- `pytest -v` - verbose output

## Output Requirements

Generate:
1. Complete test file structure as shown above
2. `conftest.py` with all necessary fixtures
3. All test modules implementing test cases from TEST_SPEC
4. `pytest.ini` or `pyproject.toml` configuration
5. Test utilities and helpers as needed
6. Mock data and fixtures

All tests should:
- Run successfully with valid source code
- Fail clearly when code is broken
- Be fast and deterministic
- Have clear, descriptive names and docstrings

## Important

Do not ask for clarification or additional information. Generate complete, production-ready test code based solely on the TEST_SPEC and SRC provided in context. Make reasonable implementation choices for any ambiguities.
