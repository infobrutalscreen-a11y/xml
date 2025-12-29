Release checklist

1. Update `CHANGELOG.md` and set the release version (e.g., `v0.1.0`).
2. Ensure tests pass locally: `python -m pytest -q tests`.
3. Push branch and open PR / merge to `main`.
4. Tag the release: `git tag -a v0.1.0 -m "v0.1.0"` and `git push origin v0.1.0`.
5. Create GitHub Release from tag and paste the changelog notes.
6. Deploy to staging, run smoke tests (curl /health and example conversions).
7. If smoke tests pass, deploy to production and monitor logs/metrics for 15 minutes.

Notes:
- If you use CI (GitHub Actions), ensure the workflow runs tests and reports status on PR.
- Keep the `feat/vk-parsers-merge` branch until the release is merged and tagged.
