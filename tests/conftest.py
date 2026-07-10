# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Pytest configuration for infra.openshift_virtualization_ops tests."""

import sys
import os

# Add the repo root to the Python path so plugins can be imported
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)
