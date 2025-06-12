# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2024-06-11

### Added

- Added quick add for reference water options

### Fixed

- Removed unwanted helper text

### Removed

- None

## [1.1.1] - 2024-06-09

### Added

- Improved the submission/search/clear forms for optimal user experience and clarity

### Fixed

- Removed the default date selection for the clear and search forms to prevent accidental deletion

### Removed

- None

## [1.1.0] - 2024-06-09

### Added

- Overhauled the Analytics and Statistics pages with new, interactive visualizations for habit completion trends and summaries.
- Streamlined the submission form for a smoother and more intuitive tracking experience.
- Added a short description under the menu on each page to clearly explain the purpose of every page.
- Enhanced the development environment to speed up the time required for subsequent releases.

### Fixed

- Improved the Last Completed page by sorting habits from oldest to newest completion, making it easier to see which habits need attention.
- Applied a hotfix to prevent the app from sleeping randomly, ensuring more reliable uptime.

### Removed

- None

## [1.0.2] - 2025-06-09

### Added 

- Improved column naming for dataframes to be more human readable
- Added reference measurements for drinking water (1 cup = 8 oz | 1 mug = 16 oz | 1 liter ≈ 34 oz | 355ml can = 12 oz | 500ml bottle ≈ 17 oz) to submission form
- Updated Search and Clear functions to show query date clearly when executing

### Fixed

- Removed extra column in Last Completed
- Updated rendering height to show all rows for Last Completed by default

## [1.0.1] - 2025-05-21

### Added 

- Added relative date column to "Last Completed"

## [1.0.0] - 2025-05-21

### Added 

- Improved response speeds for queries

### Changed

- Removed Notes section for Habit Management

### Fixed

- Updated application to use new database so that entries persist after the app timeout is exceeded

## [0.9.9] - 2025-05-01

### Added

- Initialized application:
    Added home page
    Added Stats
    Added Analytics
    Added Submission Form
    Added Last Completed
    Added Habit Manager
