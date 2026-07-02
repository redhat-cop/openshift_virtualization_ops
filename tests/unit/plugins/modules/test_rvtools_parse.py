# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for rvtools_parse module."""

import json
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def set_module_args(args):
    """Set module arguments for testing."""
    # Use environment variable to pass args for modern Ansible
    if "_ANSIBLE_ARGS" not in basic.__dict__:
        basic._ANSIBLE_ARGS = None
    if "_ANSIBLE_PROFILE" not in basic.__dict__:
        basic._ANSIBLE_PROFILE = None

    args_json = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args_json)
    basic._ANSIBLE_PROFILE = "modern"


class TestRvtoolsParseXlsx:
    def test_parse_xlsx_all_tabs(self):
        set_module_args({
            "src": os.path.join(FIXTURES_DIR, "rvtools_sample.xlsx"),
            "format": "xlsx",
        })
        with pytest.raises(SystemExit) as exc_info:
            from plugins.modules.rvtools_parse import main
            main()

        # Module exits 0 on success
        assert exc_info.value.code == 0

    def test_parse_xlsx_selected_tabs(self):
        set_module_args({
            "src": os.path.join(FIXTURES_DIR, "rvtools_sample.xlsx"),
            "format": "xlsx",
            "tabs": ["vInfo", "vCPU"],
        })
        with pytest.raises(SystemExit) as exc_info:
            from plugins.modules.rvtools_parse import main
            main()

        assert exc_info.value.code == 0

    def test_missing_file_fails(self):
        set_module_args({
            "src": "/nonexistent/file.xlsx",
            "format": "xlsx",
        })
        with pytest.raises(SystemExit) as exc_info:
            from plugins.modules.rvtools_parse import main
            main()

        assert exc_info.value.code == 1


class TestRvtoolsParseCsv:
    def test_parse_csv_single_file(self):
        set_module_args({
            "src": os.path.join(FIXTURES_DIR, "rvtools_vinfo.csv"),
            "format": "csv",
            "tabs": ["vInfo"],
        })
        with pytest.raises(SystemExit) as exc_info:
            from plugins.modules.rvtools_parse import main
            main()

        assert exc_info.value.code == 0

    def test_parse_csv_src_map(self):
        set_module_args({
            "format": "csv",
            "src_map": {
                "vInfo": os.path.join(FIXTURES_DIR, "rvtools_vinfo.csv"),
                "vCPU": os.path.join(FIXTURES_DIR, "rvtools_vcpu.csv"),
            },
        })
        with pytest.raises(SystemExit) as exc_info:
            from plugins.modules.rvtools_parse import main
            main()

        assert exc_info.value.code == 0


class TestFieldNormalization:
    def test_coerce_bool_fields(self):
        from plugins.modules.rvtools_parse import _coerce_value

        assert _coerce_value("thin", "True") is True
        assert _coerce_value("thin", "false") is False
        assert _coerce_value("connected", True) is True
        assert _coerce_value("connected", "1") is True
        assert _coerce_value("connected", "0") is False

    def test_coerce_int_fields(self):
        from plugins.modules.rvtools_parse import _coerce_value

        assert _coerce_value("cpus", "4") == 4
        assert _coerce_value("memory_mb", "8,192") == 8192
        assert _coerce_value("capacity_mb", 102400.0) == 102400
        assert _coerce_value("cpus", "") == 0
        assert _coerce_value("cpus", None) is None

    def test_coerce_string_fields(self):
        from plugins.modules.rvtools_parse import _coerce_value

        assert _coerce_value("vm_name", "  web-01  ") == "web-01"
        assert _coerce_value("vm_name", None) is None
