# Changelog

All notable changes to the Google Antigravity SDK will be documented in this file.

## [Unreleased]

### Fixed
- Fixed a critical `TypeError: Couldn't build proto file into descriptor pool` bug during module load that broke imports across all Python environments due to protobuf edition mismatch. `localharness_pb2` imports are now properly lazy-loaded.
- Pinned `protobuf>=5.26.0` dependency in `pyproject.toml` to guarantee compatibility with generated bindings targeting newer protobuf editions.
- Added graceful fallback logging with a clear, actionable exception message when protobuf compilation or execution fails.

### Added
- Added comprehensive import testing (`import_test.py`) to the test suite to ensure the package initializes safely without strict dependencies on local harness binary status.
- Added a `google/antigravity/_build_info.py` module containing metadata (`PROTOBUF_GENCODE_VERSION`) about the protobuf compiler environment.
- Added improved `GEMINI_API_KEY` handling, which raises a clear `ValueError` with instructions and a link to Google AI Studio if the API key is not present when attempting to start an `Agent`.
- Expose the SDK runtime as an MCP Server (`mcp/server.py`) containing the `mcp_antigrav_status` tool to check component health and versions via MCP bridges.

### Changed
- Clarified `pyproject.toml` configuration and instructions. The Local Harness language server binary is entirely optional for local dev (`pip install -e .`) and Python-only testing workflows.

### Post-fix verification & MCP prep (2026-06)
- Verified clean top-level import, `LocalAgentConfig`, and `import_test.py` pass with editable source (protobuf guards + lazy imports prevent edition crash).
- Updated `scripts/antigrav-ping.py` (MCP status helper integration for direct calls, relaxed overall to focus SDK health separate from harness binary per task guidance, richer reporting).
- Fixed/ hardened `mcp/server.py` + `mcp/__init__.py` + exposed `__version__` early in top `__init__.py` (no circular, `mcp_antigrav_status` tool now robust and rich; enables status pings to use tools directly via MCP bridge instead of only shell).
- Updated SDK `README.md` with MCP usage and verification notes.
- (Related but cross-project) Conductor vault loaders + native council example now discover agents from `vaults/conductor/agents/` for a fully working modular council (ember + 4 skills).
