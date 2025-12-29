# Changelog

## Unreleased (unreleased)

- feat: add VK converters and endpoints (auto, goods, avia, hotel, estate, service)
- feat: XML renderers for avia/estate/hotel/service
- feat: soft validation for goods/auto (JSON warnings + headers)
- fix: lazy PyYAML import to avoid startup crash when missing
- test: add regression and edge-case tests for parsing and VK endpoints
- docs: add VK endpoint examples in README

---

## [Unreleased] - Prepare release v0.1.0 (2025-12-30)

Planned release items:
- Merge and squash `feat/vk-parsers-merge` into `main`.
- Ensure all tests pass in CI (pytest).
- Tag release: `v0.1.0` and create GitHub Release with CHANGES.
- Deploy to staging and run smoke tests (health endpoint + sample requests).
