# Reflectly Roadmap

This document defines the development roadmap for Reflectly.
The goal is to deliver a stable MVP before adding advanced features.

---

## Phase 1: Backend CRUD (Core Stability)

Goal: Ensure the backend API fully supports required operations
for users and sessions with correct business rules.

### User
- [x] Update user profile (username, email)
- [x] Delete user account (soft delete allowed)

### Sessions
- [x] Update session
  - title
  - description
  - start_time
  - end_time
- [x] Delete session

### Business Rules
- [ ] Enforce single active session per user
- [ ] Prevent access to other users’ sessions
- [ ] Define active session as `end_time = null`

Deliverable:
- Fully functional CRUD API for users and sessions
- No frontend dependencies

---

## Phase 2: Frontend CRUD Integration

Goal: Expose all backend CRUD functionality through the UI.

### Dashboard Layout
- [ ] Dashboard base layout
- [ ] Tabs: Sessions / Profile

### Sessions
- [ ] Sessions list
- [ ] Click session to open edit modal
- [ ] Update session from modal
- [ ] Delete session with confirmation

### Timer
- [ ] Start session
- [ ] Stop session
- [ ] Disable start when an active session exists

### Profile
- [ ] Edit user profile
- [ ] Delete user account

Deliverable:
- All backend features accessible via UI
- Functional and usable interface (visual polish not required)

---

## Phase 3: Projects Support

Goal: Organize sessions by projects without breaking MVP stability.

### Backend
- [ ] Create project
- [ ] List projects
- [ ] Delete project

### Sessions
- [ ] Attach session to a project (project_id nullable)

### Frontend
- [ ] Project selector in session edit modal
- [ ] Filter sessions by project

Deliverable:
- Sessions grouped by projects
- Improved organization and clarity for users

---

## Out of Scope for MVP

The following features are intentionally excluded until all phases
above are completed:

- AI analysis
- Mood tracking
- Advanced statistics and charts
- Calendar integrations
- Animations and visual effects

---

## Development Rules

- Only one active phase at a time
- Only one task in progress at a time
- No new entities before existing ones have full CRUD
- Each task should map to a single, logical commit
