# Changelog
All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2025-12-12
### Added
- Added `templeton/static/` dir
- Added `main.css`

---

## [1.1.0] - 2025-12-29
### Added
- Created `getFormData()`, `getEnumData()`, `getMetadata()`, `createURL()` functions.
- Added `<fieldset class="form {{ title }}">` to the form template to style it better.
- Added `<table class="data {{ title }}">` to the report template to style it better.
- Create new module: `formulator.helper`,

---

## [1.2.0] - 2026-02-22
### Changed
- Changed `formulator.logic` to `formulator.generator` and add `Generator()` class to it.
- Moved `toolkit.DB` to `formulator.DB` and added `formulator.helper` within the class.

### Added
- Added `DataHandler` class.
- Added docstrings for `DataHandler` class.
- Started work on a CLI version.
- Added `tests`, `scripts`, `examples` directories.

---

---

## [1.2.1] - 2026-03-31
### Changed
- Found some bugs in the `pyproject.toml` file

---

## Legend
- **Added** — new features.  
- **Changed** — changes in existing functionality.  
- **Deprecated** — features soon-to-be removed.  
- **Removed** — removed features.  
- **Fixed** — bug fixes.  
- **Security** — security fixes.

---
