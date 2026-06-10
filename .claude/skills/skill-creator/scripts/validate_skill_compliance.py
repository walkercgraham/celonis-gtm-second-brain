#!/usr/bin/env python3
"""
Validate that Celonis skills use celonis_generator functions properly
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set


class SkillComplianceValidator:
    """Validates that skills use celonis_generator properly."""

    def __init__(self):
        self.required_imports = {
            'ocdm': {
                'celonis_generator.generators.ocdm_package',
                'celonis_generator.exporters',
                'celonis_generator.config.validator'
            },
            'frontend': {
                'celonis_generator.generators.studio',
                'celonis_generator.exporters'
            },
        }

        self.prohibited_patterns = [
            r'def\s+generate_\w+_package\s*\(',  # Custom generation functions
            r'def\s+create_\w+_zip\s*\(',        # Custom ZIP creation
            r'def\s+export_\w+\s*\(',            # Custom export functions
            r'manifest\s*=\s*\{',                # Manual manifest creation
            r'variables\s*=\s*\{',               # Manual variables creation
        ]

    def validate_skill(self, skill_path: Path) -> Dict:
        """Validate a single skill directory."""
        results = {
            'skill_name': skill_path.name,
            'compliant': True,
            'issues': [],
            'files_checked': []
        }

        # Check Python files in scripts/ (skip test files)
        scripts_dir = skill_path / 'scripts'
        if scripts_dir.exists():
            for py_file in scripts_dir.glob('*.py'):
                # Skip test files - they don't need to use exporters
                if py_file.name.startswith('test_'):
                    continue
                # Skip utility scripts that don't generate packages
                if py_file.name in ['project_manager.py', 'context_mapper.py', 'validation_checker.py']:
                    continue
                file_results = self._validate_python_file(py_file, skill_path.name)
                results['files_checked'].append(py_file.name)
                if not file_results['compliant']:
                    results['compliant'] = False
                    results['issues'].extend([
                        f"{py_file.name}: {issue}" for issue in file_results['issues']
                    ])

        return results

    def _validate_python_file(self, py_file: Path, skill_type: str) -> Dict:
        """Validate a single Python file."""
        results = {'compliant': True, 'issues': []}

        try:
            with open(py_file, 'r') as f:
                content = f.read()

            # Check for required imports
            if skill_type in self.required_imports:
                missing_imports = self._check_imports(content, skill_type)
                if missing_imports:
                    results['compliant'] = False
                    results['issues'].extend([
                        f"Missing required import: {imp}" for imp in missing_imports
                    ])

            # Check for prohibited patterns
            prohibited_found = self._check_prohibited_patterns(content)
            if prohibited_found:
                results['compliant'] = False
                results['issues'].extend([
                    f"Found prohibited pattern: {pattern}" for pattern in prohibited_found
                ])

            # Check for proper generator usage
            generator_issues = self._check_generator_usage(content, skill_type)
            if generator_issues:
                results['compliant'] = False
                results['issues'].extend(generator_issues)

        except Exception as e:
            results['compliant'] = False
            results['issues'].append(f"Error reading file: {e}")

        return results

    def _check_imports(self, content: str, skill_type: str) -> List[str]:
        """Check for required imports."""
        required = self.required_imports.get(skill_type, set())
        missing = []

        for req_import in required:
            # Check various import patterns
            patterns = [
                f"from {req_import} import",
                f"import {req_import}"
            ]

            if not any(pattern in content for pattern in patterns):
                missing.append(req_import)

        return missing

    def _check_prohibited_patterns(self, content: str) -> List[str]:
        """Check for prohibited custom implementation patterns."""
        found = []

        for pattern in self.prohibited_patterns:
            if re.search(pattern, content, re.MULTILINE):
                found.append(pattern)

        return found

    def _check_generator_usage(self, content: str, skill_type: str) -> List[str]:
        """Check for proper generator class usage."""
        issues = []

        # Expected generator classes
        expected_generators = {
            'ocdm': 'OCDMPackageGenerator',
            'frontend': 'PlanDrivenAppGenerator',
        }

        if skill_type in expected_generators:
            expected_gen = expected_generators[skill_type]
            if expected_gen not in content:
                issues.append(f"Should use {expected_gen} class")

        # Check for proper exporter usage
        exporter_patterns = ['export_to_directory', 'export_to_zip']
        if not any(pattern in content for pattern in exporter_patterns):
            issues.append("Should use official exporter methods")

        return issues

    def validate_all_skills(self) -> Dict:
        """Validate all Celonis skills."""
        skills_dir = Path(__file__).parent
        results = {
            'total_skills': 0,
            'compliant_skills': 0,
            'skills': []
        }

        # Find Celonis-related skills (updated for studio-plan/studio-package split)
        celonis_skills = [
            'data-discovery',
            'ocdm-modeling',
            'ocdm-package',
            'ocdm-sql',
            'ocdm-deploy',
            'studio-km',
            'studio-plan',      # View planning (from studio-views split)
            'studio-package',   # Package generation (from studio-views split)
            'studio-pql',
            'e2e-implementation',
        ]

        for skill_name in celonis_skills:
            skill_path = skills_dir / skill_name
            if skill_path.exists():
                skill_results = self.validate_skill(skill_path)
                results['skills'].append(skill_results)
                results['total_skills'] += 1
                if skill_results['compliant']:
                    results['compliant_skills'] += 1

        return results

    def print_report(self, results: Dict):
        """Print compliance report."""
        print("🔍 Celonis Skill Compliance Report")
        print("=" * 50)

        total = results['total_skills']
        compliant = results['compliant_skills']
        print(f"📊 Summary: {compliant}/{total} skills compliant")

        for skill in results['skills']:
            status = "✅" if skill['compliant'] else "❌"
            print(f"\n{status} {skill['skill_name']}")

            if skill['files_checked']:
                print(f"   Files checked: {', '.join(skill['files_checked'])}")

            if not skill['compliant']:
                print("   Issues:")
                for issue in skill['issues']:
                    print(f"     - {issue}")

        print(f"\n{'✅ All skills compliant!' if compliant == total else '❌ Some skills need fixes'}")


def main():
    """Run compliance validation."""
    validator = SkillComplianceValidator()
    results = validator.validate_all_skills()
    validator.print_report(results)

    # Return exit code for CI/CD
    return 0 if results['compliant_skills'] == results['total_skills'] else 1


if __name__ == "__main__":
    exit(main())