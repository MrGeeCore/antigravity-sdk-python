# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for pure Python import behavior."""

import unittest

class ImportTest(unittest.TestCase):

    def test_clean_import_and_basic_config(self):
        """Verify the SDK can be imported and configured without harness crashes."""
        import google.antigravity
        from google.antigravity import Agent, LocalAgentConfig
        
        cfg = LocalAgentConfig(system_instructions="sanity")
        self.assertIsNotNone(cfg)

if __name__ == '__main__':
    unittest.main()
