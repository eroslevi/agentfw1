"""
CHK - Check and Fix Mechanism

This module implements the check mechanism that:
1. Runs the test suite
2. If all tests pass, returns successfully
3. If tests fail, attempts to fix the source code using the LLM
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Tuple, Optional
import json
from datetime import datetime


class CheckMechanism:
    """
    Mechanism for running tests and fixing failing code.
    
    This class orchestrates the testing and fixing process:
    1. Runs test suite (pytest)
    2. Collects test failure information
    3. Uses LLM to generate fixes
    4. Applies fixes to source code
    5. Reruns tests to verify fixes
    """
    
    def __init__(
        self,
        system_path: str,
        test_dir: str = "tests",
        src_dir: str = "src",
        max_fix_attempts: int = 3,
        llm_client = None
    ):
        """
        Initialize the check mechanism.
        
        Args:
            system_path: Path to the generated system directory.
            test_dir: Name of the tests directory (relative to system_path).
            src_dir: Name of the source directory (relative to system_path).
            max_fix_attempts: Maximum number of fix attempts before giving up.
            llm_client: Optional LLM client for code fixing. If not provided,
                       only reports test failures without attempting fixes.
        """
        self.system_path = Path(system_path)
        self.test_dir = self.system_path / test_dir
        self.src_dir = self.system_path / src_dir
        self.max_fix_attempts = max_fix_attempts
        self.llm_client = llm_client
        self.fix_attempts = 0
        self.fix_history = []
    
    def run_tests(self, verbose: bool = True) -> Tuple[bool, str]:
        """
        Run the test suite using pytest.
        
        Args:
            verbose: Whether to print verbose output.
        
        Returns:
            Tuple of (all_tests_passed: bool, output: str)
        """
        if not self.test_dir.exists():
            return False, f"Test directory not found: {self.test_dir}"
        
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir),
            "-v",
            "--tb=short"
        ]
        
        if verbose:
            cmd.append("--capture=no")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.system_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            output = result.stdout + result.stderr
            passed = result.returncode == 0
            
            return passed, output
        
        except subprocess.TimeoutExpired:
            return False, "Test suite execution timed out after 300 seconds"
        except Exception as e:
            return False, f"Error running tests: {str(e)}"
    
    def parse_test_failures(self, test_output: str) -> dict:
        """
        Parse test output to extract failure information.
        
        Args:
            test_output: Raw output from pytest.
        
        Returns:
            Dictionary containing failure information.
        """
        failures = {
            "failed_tests": [],
            "error_messages": [],
            "raw_output": test_output
        }
        
        lines = test_output.split("\n")
        for i, line in enumerate(lines):
            if "FAILED" in line or "ERROR" in line:
                failures["failed_tests"].append(line)
            if "AssertionError" in line or "Exception" in line:
                failures["error_messages"].append(line)
        
        return failures
    
    def get_source_files(self) -> list:
        """
        Get list of Python source files to potentially fix.
        
        Returns:
            List of Path objects for Python files in src directory.
        """
        if not self.src_dir.exists():
            return []
        
        return list(self.src_dir.rglob("*.py"))
    
    def generate_fix_prompt(
        self,
        failure_info: dict,
        tech_spec_path: Optional[str] = None
    ) -> str:
        """
        Generate a prompt for the LLM to fix the code.
        
        Args:
            failure_info: Dictionary containing test failure information.
            tech_spec_path: Optional path to the technical specification.
        
        Returns:
            Prompt string for the LLM.
        """
        prompt = f"""The test suite has failed with the following errors:

## Failed Tests:
{chr(10).join(failure_info.get('failed_tests', []))}

## Error Messages:
{chr(10).join(failure_info.get('error_messages', []))}

## Test Output:
{failure_info.get('raw_output', '')[:2000]}

## Task:
Analyze the test failures and suggest fixes to the source code that would make the tests pass.
Consider:
1. What the tests are expecting
2. What the current code is doing wrong
3. How to fix the code to meet test expectations

Provide specific code changes with line numbers and explanations."""
        
        if tech_spec_path and os.path.exists(tech_spec_path):
            with open(tech_spec_path, 'r') as f:
                tech_spec = f.read()
            prompt += f"\n\n## Technical Specification:\n{tech_spec[:2000]}"
        
        return prompt
    
    def apply_fixes(self, fix_suggestions: str) -> bool:
        """
        Apply code fixes based on LLM suggestions.
        
        This is a placeholder that logs fix suggestions.
        In a production system, this would parse the LLM suggestions
        and apply them to the source files.
        
        Args:
            fix_suggestions: Suggestions from the LLM.
        
        Returns:
            Whether fixes were applied.
        """
        fix_record = {
            "timestamp": datetime.now().isoformat(),
            "attempt": self.fix_attempts,
            "suggestions": fix_suggestions
        }
        self.fix_history.append(fix_record)
        
        print(f"\n{'='*60}")
        print(f"FIX ATTEMPT #{self.fix_attempts}")
        print(f"{'='*60}")
        print("LLM Suggestions:")
        print(fix_suggestions)
        print(f"{'='*60}\n")
        
        # In a real implementation, this would parse the suggestions and apply them
        # For now, it logs them for manual application
        
        return True
    
    def check(
        self,
        tech_spec_path: Optional[str] = None,
        auto_fix: bool = False
    ) -> Tuple[bool, str]:
        """
        Run the complete check process: test, analyze failures, and optionally fix.
        
        Args:
            tech_spec_path: Optional path to technical specification for context.
            auto_fix: Whether to attempt automatic fixes using LLM.
        
        Returns:
            Tuple of (success: bool, summary: str)
        """
        print(f"Starting check process for system at: {self.system_path}")
        print(f"Max fix attempts: {self.max_fix_attempts}")
        print()
        
        # Run initial tests
        print("Step 1: Running test suite...")
        all_passed, test_output = self.run_tests()
        
        if all_passed:
            summary = "✓ All tests passed! No fixes needed."
            print(summary)
            return True, summary
        
        print(f"\n✗ {test_output.count('FAILED')} test(s) failed")
        
        # If no LLM client or auto_fix disabled, just report failures
        if not self.llm_client or not auto_fix:
            summary = f"Tests failed. Fix attempts disabled. Output:\n{test_output}"
            return False, summary
        
        # Attempt to fix
        print(f"\nStep 2: Attempting automatic fixes (max {self.max_fix_attempts} attempts)...\n")
        
        while self.fix_attempts < self.max_fix_attempts:
            self.fix_attempts += 1
            
            # Parse failures
            failure_info = self.parse_test_failures(test_output)
            
            # Generate fix prompt
            fix_prompt = self.generate_fix_prompt(failure_info, tech_spec_path)
            
            # Get LLM suggestions
            try:
                suggestions = self.llm_client.generate_from_prompt(
                    system_prompt="You are an expert Python developer fixing failing tests.",
                    user_prompt=fix_prompt
                )
            except Exception as e:
                return False, f"LLM error during fix attempt: {str(e)}"
            
            # Apply fixes
            self.apply_fixes(suggestions)
            
            # Rerun tests
            print(f"Rerunning tests after fix attempt {self.fix_attempts}...")
            all_passed, test_output = self.run_tests(verbose=False)
            
            if all_passed:
                summary = f"✓ All tests passed after {self.fix_attempts} fix attempt(s)!"
                print(summary)
                return True, summary
            else:
                remaining = self.max_fix_attempts - self.fix_attempts
                print(f"✗ Tests still failing. {remaining} attempt(s) remaining.\n")
        
        summary = f"✗ Tests failed after {self.max_fix_attempts} fix attempts. Manual intervention required."
        print(summary)
        
        return False, summary
    
    def get_fix_history(self) -> list:
        """
        Get the history of fix attempts.
        
        Returns:
            List of fix attempt records.
        """
        return self.fix_history
    
    def save_report(self, output_path: str) -> None:
        """
        Save a report of the check process.
        
        Args:
            output_path: Path where to save the report.
        """
        report = {
            "system_path": str(self.system_path),
            "timestamp": datetime.now().isoformat(),
            "fix_attempts": self.fix_attempts,
            "max_fix_attempts": self.max_fix_attempts,
            "fix_history": self.fix_history
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)


def run_check(
    system_path: str,
    tech_spec_path: Optional[str] = None,
    auto_fix: bool = True,
    llm_client = None
) -> Tuple[bool, str]:
    """
    Convenience function to run the check mechanism.
    
    Args:
        system_path: Path to the generated system directory.
        tech_spec_path: Optional path to technical specification.
        auto_fix: Whether to attempt automatic fixes.
        llm_client: Optional LLM client for automatic fixes.
    
    Returns:
        Tuple of (success: bool, summary: str)
    """
    checker = CheckMechanism(
        system_path=system_path,
        llm_client=llm_client,
        max_fix_attempts=3
    )
    
    return checker.check(
        tech_spec_path=tech_spec_path,
        auto_fix=auto_fix
    )
