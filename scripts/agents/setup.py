#!/usr/bin/env python3
"""Interactive setup wizard for the agent system.

Creates _agents/config.yaml from config-template.yaml by prompting for
required values, and copies regions-template.yaml if needed.
"""
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE = os.path.join(REPO, "_agents", "config-template.yaml")
CONFIG = os.path.join(REPO, "_agents", "config.yaml")
REGIONS_TEMPLATE = os.path.join(REPO, "_agents", "account-watch", "regions-template.yaml")
REGIONS = os.path.join(REPO, "_agents", "account-watch", "regions.yaml")


def ask(prompt, default="", validator=None, required=True):
    while True:
        suffix = f" [{default}]" if default else ""
        answer = input(f"  {prompt}{suffix}: ").strip()
        if not answer and default:
            answer = default
        if required and not answer:
            print("    → Required. Please enter a value.")
            continue
        if validator and answer:
            err = validator(answer)
            if err:
                print(f"    → {err}")
                continue
        return answer


def validate_slack_id(v):
    if not re.match(r'^[A-Z][A-Z0-9]{8,}$', v):
        return "Slack IDs look like U0123456789 or C0123456789 (uppercase letters + digits)."
    return None


def validate_timezone(v):
    if "/" not in v:
        return "Use IANA format: e.g. America/New_York, Europe/London, Asia/Dubai"
    return None


def validate_path(v):
    expanded = os.path.expanduser(v)
    if not os.path.isdir(expanded):
        return f"Directory not found: {expanded}"
    return None


def confirm(prompt):
    answer = input(f"  {prompt} [Y/n]: ").strip().lower()
    return answer in ("", "y", "yes")


def main():
    print()
    print("=" * 60)
    print("  Agent System Setup")
    print("=" * 60)
    print()

    if os.path.exists(CONFIG):
        if not confirm("config.yaml already exists. Overwrite it?"):
            print("  Keeping existing config.yaml.")
            print()
            setup_regions()
            print_next_steps()
            return
        print()

    if not os.path.exists(TEMPLATE):
        print(f"  ERROR: config-template.yaml not found at {TEMPLATE}")
        sys.exit(1)

    with open(TEMPLATE) as f:
        config = f.read()

    print("  I'll ask a few questions to set up your config.yaml.")
    print("  (You can always edit _agents/config.yaml later.)")
    print()

    print("  ── Slack ──")
    print()
    slack_self = ask(
        "Your Slack member ID (profile → ⋯ → Copy member ID)",
        validator=validate_slack_id,
        required=False,
    )
    slack_agent = ask(
        "Slack channel ID for agent output (create a private channel first)",
        validator=validate_slack_id,
        required=False,
    )
    slack_capture = ask(
        "Slack channel ID for quick captures (optional, for capture-keeper)",
        validator=validate_slack_id,
        required=False,
    )
    print()

    print("  ── General ──")
    print()
    timezone = ask(
        "Your timezone (IANA format)",
        default="Europe/London",
        validator=validate_timezone,
    )
    vault_path = ask(
        "Absolute path to this vault",
        default=REPO,
        validator=validate_path,
    )
    print()

    replacements = {
        'slack_self_user_id: ""': f'slack_self_user_id: "{slack_self}"',
        'slack_agent_channel_id: ""': f'slack_agent_channel_id: "{slack_agent}"',
        'slack_capture_channel_id: ""': f'slack_capture_channel_id: "{slack_capture}"',
        'timezone: ""': f'timezone: "{timezone}"',
        'vault_path: ""': f'vault_path: "{vault_path}"',
    }

    for old, new in replacements.items():
        config = config.replace(old, new)

    with open(CONFIG, "w") as f:
        f.write(config)

    print(f"  ✓ Created _agents/config.yaml")
    print()

    setup_regions()
    print_next_steps()


def setup_regions():
    if os.path.exists(REGIONS):
        print(f"  ✓ regions.yaml already exists (skipping copy)")
    elif os.path.exists(REGIONS_TEMPLATE):
        shutil.copy2(REGIONS_TEMPLATE, REGIONS)
        print(f"  ✓ Copied regions-template.yaml → regions.yaml")
        print(f"    Edit _agents/account-watch/regions.yaml to activate your regions.")
    else:
        print(f"  ⚠ regions-template.yaml not found — skipping.")
    print()


def print_next_steps():
    print("  ── Next Steps ──")
    print()
    print("  1. Review _agents/config.yaml and adjust schedules to your timezone")
    print("  2. Add agent frontmatter to your client hub files (email_domains, slack_channels, etc.)")
    print("  3. Activate your regions in _agents/account-watch/regions.yaml")
    print("  4. Register scheduled tasks with Claude Code (see _agents/scheduled-tasks.md)")
    print("  5. All agents start in shadow mode — review shadow output for 1–2 weeks before going live")
    print()
    print("  See _agents/README.md for full documentation.")
    print()


if __name__ == "__main__":
    main()
