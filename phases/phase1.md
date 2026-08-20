# Phase 1 — Problem Definition & Data Foundation

## Epic Goal

Establish a clear, reproducible foundation for the Dubai house price prediction project before starting feature engineering or model development.

## Issues

### 1. Define Prediction Objective & Success Criteria

**Goal:** Clearly define what the model is predicting and how success will be measured.

**Tasks:**

- Define prediction target
- Define prediction unit
- Define what constitutes a valid sale
- Define prediction-time information boundary
- Select primary evaluation metric
- Select secondary evaluation metrics
- Define initial success criteria

**Deliverable:**

- Problem definition documented in `docs/problem-definition.md`

---

### 2. Audit Raw Dubai Property Dataset

**Goal:** Understand the raw data before making any transformations.

**Tasks:**

- Document dataset source and provenance
- Inspect schema and data types
- Determine row count and date range
- Understand geographic coverage
- Analyze missing values
- Identify duplicates
- Identify invalid/suspicious values
- Identify potential target leakage
- Identify repeated properties/transactions

**Deliverable:**

- Data audit report
- Initial data quality findings

---

### 3. Create Data Dictionary & Data Contract

**Goal:** Define the expected structure and semantics of the dataset.

**Tasks:**

- Document important columns
- Define data types
- Define required vs optional fields
- Define valid ranges/constraints
- Document categorical values where appropriate
- Mark whether each feature is available at prediction time
- Identify fields that must never be used for prediction

**Deliverable:**

- `docs/data-dictionary.md`
- Version-controlled data schema/contract

---

### 4. Design Train / Validation / Test Strategy

**Goal:** Define a realistic evaluation strategy before model development.

**Tasks:**

- Decide temporal vs random splitting
- Define train/validation/test periods
- Determine how repeated properties are handled
- Define leakage prevention rules
- Document rationale for the chosen strategy

**Deliverable:**

- Documented dataset splitting strategy
- Initial split implementation if appropriate

---

### 5. Set Up ML Repository & Development Environment

**Goal:** Create a clean engineering foundation that both engineers can work from.

**Tasks:**

- Establish repository structure
- Set up Python/package management
- Add dependency management
- Add configuration approach
- Add formatting/linting
- Add testing framework
- Add basic project documentation
- Establish Git/branch/PR conventions

**Deliverable:**

- Reproducible local development environment
- Clean repository structure

---

### 6. Set Up CI Foundation

**Goal:** Ensure code quality checks happen automatically.

**Tasks:**

- Add GitHub Actions workflow
- Run automated tests
- Run linting/formatting checks
- Verify project installation
- Ensure CI runs on pull requests

**Deliverable:**

- Passing CI pipeline on GitHub

---

### 7. Document Phase 1 Decisions

**Goal:** Capture important decisions so future contributors understand the reasoning.

**Tasks:**

- Document prediction objective
- Document data assumptions
- Document evaluation strategy
- Document data contract
- Document known limitations
- Record important architecture/design decisions

**Deliverable:**

- Updated `README.md`
- `docs/` containing Phase 1 documentation

---

## Phase 1 Definition of Done

- [ ] Prediction objective is clearly defined
- [ ] Success metrics are agreed upon
- [ ] Raw dataset has been audited
- [ ] Potential leakage has been identified
- [ ] Data dictionary/data contract exists
- [ ] Train/validation/test strategy is defined
- [ ] Repository and development environment are reproducible
- [ ] Basic CI is working
- [ ] Important decisions and assumptions are documented
- [ ] Both engineers have reviewed the Phase 1 outputs

## Collaboration Model

For each issue:

**1 Engineer = Owner**  
**1 Engineer = Reviewer**

Swap ownership/reviewer roles across issues and phases so both engineers gain experience across data, ML, testing, and production engineering.

## Phase 1 Output

At the end of Phase 1, we should be able to confidently answer:

> **What exactly are we predicting, what data are we allowed to use, how will we evaluate the model, and can another engineer reproduce our development environment?**
