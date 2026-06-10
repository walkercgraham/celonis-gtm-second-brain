# Skill Template - celonis_generator Integration

## Required Structure for Celonis Skills

All Celonis skills MUST use `celonis_generator` functions rather than custom generation logic.

### Skill Directory Structure
```
skill-name/
├── SKILL.md                    # Workflow documentation
├── scripts/
│   ├── generate_[type].py      # ✅ Uses celonis_generator
│   └── validate_[type].py      # ✅ Uses celonis_generator validators
└── references/                 # Supporting documentation
```

### Required Imports Pattern
```python
# ✅ CORRECT - Use celonis_generator
from celonis_generator.generators.[type] import [Generator]
from celonis_generator.exporters import [Exporter]
from celonis_generator.config.validator import ProjectConfig

# ❌ INCORRECT - No custom generation logic
# def custom_generate_package(): ...
```

### Validation Requirements
1. **Use ProjectConfig** - All skills must work with standardized config
2. **Use Official Generators** - No custom generation logic
3. **Use Official Exporters** - No custom export/packaging
4. **Handle Errors Properly** - Use generator error handling

### Generator Mappings
| Skill Type | Required Generator | Required Exporter |
|------------|-------------------|-------------------|
| ocdm | `OCDMPackageGenerator` | `OCDMPackageExporter` |
| frontend | `PlanDrivenAppGenerator` | `StudioAppExporter` |
| pool | `DataPoolGenerator` | `JSONExporter` |

### Example Implementation
```python
#!/usr/bin/env python3
"""
Skill: [skill-name]
Uses: celonis_generator.[generator-type]
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

# ✅ REQUIRED: Use celonis_generator
from celonis_generator.generators.[type] import [GeneratorClass]
from celonis_generator.exporters import [ExporterClass]
from celonis_generator.config.validator import ProjectConfig

def generate_[type](project_path: Path):
    """Generate [type] using validated celonis_generator functions."""

    # 1. Load/create ProjectConfig
    config = create_project_config(project_path)

    # 2. Use official generator
    generator = [GeneratorClass](config)

    # 3. Use official exporter
    exporter = [ExporterClass](config)
    result = exporter.export_to_directory(output_path)

    return result

if __name__ == "__main__":
    generate_[type](Path.cwd())
```