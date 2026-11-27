## ADDED Requirements

### Requirement: Protected default branch
The default branch SHALL only change through pull requests, SHALL keep a linear history, and MUST NOT allow force pushes or deletion.

#### Scenario: the default branch only changes through pull requests
- **GIVEN** the repository's default branch
- **WHEN** its active rules are listed
- **THEN** they include `pull_request`, `non_fast_forward`, `deletion` and `required_linear_history`

### Requirement: Linear history that keeps TDD commits
The repository SHALL disable merge commits, SHALL allow rebase merges so that red → green → refactor commits are preserved on the default branch, and SHALL delete head branches after merge.

#### Scenario: history stays linear and branches are cleaned up
- **GIVEN** the repository settings
- **WHEN** they are read
- **THEN** rebase merge is allowed, merge commits are disabled, and branches are deleted on merge

### Requirement: Private vulnerability reporting
The repository SHALL accept private vulnerability reports, publish a security policy, and keep secret scanning push protection on.

#### Scenario: vulnerabilities can be reported privately
- **GIVEN** the repository security settings
- **WHEN** they are read
- **THEN** private vulnerability reporting and secret scanning push protection are enabled
- **AND** `SECURITY.md` exists on the default branch

### Requirement: Ownership and review checklist
The repository SHALL define code owners and a pull request template.

#### Scenario: governance files exist on the default branch
- **GIVEN** the default branch
- **WHEN** its files are listed
- **THEN** `.github/CODEOWNERS` and `.github/pull_request_template.md` exist

<!-- TODO (learner): your PR template's checklist is part of the spec.
     Add a requirement listing what every PR must confirm
     (spec updated, tests first, docs, security checklist, and so on).
     Then run: openspec validate add-repository-security-baseline --strict -->
