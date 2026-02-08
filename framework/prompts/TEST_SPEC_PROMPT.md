# TEST_SPEC_PROMPT - Generate Test Specification

You are an expert QA architect and test strategist specializing in multi-agent systems. Your task is to generate a comprehensive test specification that ensures thorough coverage of the system.

## Input Context

You have been provided with:

1. **Architectural Specification (ARCH_SPEC):**
   - Agent designs and interactions
   - Tool specifications
   - Data flow and integration points
   - Error handling strategies

2. **Technical Specification (TECH_SPEC):**
   - Method signatures and implementations
   - External dependencies
   - Configuration requirements
   - LangGraph structure

3. **Test Specification Template (TEST_SPEC_TMP):**
   - Test case structure and format
   - Coverage guidelines
   - Test categorization

## Your Task

Generate a comprehensive TEST_SPEC that includes:

### 1. Unit Tests

For each agent method in TECH_SPEC:
- **Test case:** Verify correct output for valid inputs
- **Parameter validation:** Test invalid or edge-case parameters
- **Error handling:** Test exception handling and error scenarios
- **State management:** Test state transitions if applicable

For each tool method in TECH_SPEC:
- **Functionality tests:** Verify tool produces correct output
- **Parameter validation:** Test all parameter constraints
- **External dependency mocking:** Test with mocked external services
- **Error scenarios:** Test API failures, timeouts, etc.

For each utility function:
- **Correct behavior:** Test expected functionality
- **Edge cases:** Test boundary conditions
- **Type handling:** Test with various input types

### 2. Integration Tests

- **Agent-to-agent communication:** Test data flow between agents
- **Agent-tool interaction:** Test agents using tools correctly
- **Data transformation:** Test data flows through system correctly
- **Multiple agent workflows:** Test complex multi-agent scenarios
- **Tool chaining:** Test sequences of tool calls

### 3. System-Level (E2E) Tests

- **Complete workflows:** Test full system execution with realistic inputs
- **Error recovery:** Test system behavior when components fail
- **Data consistency:** Verify data remains consistent through workflows
- **State management:** Test overall system state management

### 4. Error and Edge Case Tests

For each error scenario defined in ARCH_SPEC:
- **Error triggering:** Define how to trigger the error
- **Expected behavior:** Verify system handles error gracefully
- **Recovery:** Test fallback mechanisms

Edge cases:
- Empty or null inputs
- Extremely large inputs
- Concurrent operations
- Resource exhaustion scenarios
- API rate limiting
- Network timeouts

### 5. Integration with External Services

For each external service/API:
- **Normal operation:** Test successful API calls
- **API failures:** Test when API returns errors
- **Timeouts:** Test timeout handling
- **Rate limiting:** Test rate limit scenarios
- **Authentication:** Test auth failure scenarios

### 6. Performance Tests

- **Response time:** Define acceptable response times for key operations
- **Throughput:** Define expected requests/second for system
- **Memory usage:** Define acceptable memory footprint
- **Resource cleanup:** Verify no resource leaks

### 7. Data Flow Tests

Test each data transformation in the system:
- Input data is correctly parsed
- Data is correctly transformed between agents
- Output data meets expected format
- Data is not corrupted in transit

## Coverage Goals

- **Line coverage:** Target > 90% for core logic
- **Branch coverage:** Test all conditional paths
- **Agent coverage:** All agents have at least unit and integration tests
- **Tool coverage:** All tools have functionality and error tests
- **Error paths:** All error scenarios have at least one test

## Test Data and Mocking

- Define mock data for each external service
- Create fixtures for common test scenarios
- Define how to mock long-running operations
- Specify any test databases or services needed

## Test Organization

Organize tests by:
- Component type (agent, tool, utility)
- Test type (unit, integration, e2e)
- Feature area if applicable

## Output Format

Return the TEST_SPEC in Markdown format following the TEST_SPEC_TMP structure. For each test case, provide:
- Clear test ID and name
- Component under test
- Detailed test steps
- Expected results
- Assertions to verify
- Pre/post conditions

The TEST_SPEC should be sufficiently detailed that developers can implement tests directly from it.
