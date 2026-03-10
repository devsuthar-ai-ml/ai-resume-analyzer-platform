# AI Resume Analyzer Platform

Frontend-first documentation for the complete UI experience (without screenshots).

## Frontend UI Overview

This platform UI is designed as a professional workflow:

1. User lands on marketing/intro page.
2. User signs up or logs in.
3. User opens dashboard and checks resume history.
4. User uploads resume + enters job description.
5. User sees AI analysis report with score, match %, skills, and suggestions.

## Frontend Tech Stack

- React 19
- TypeScript
- Tailwind CSS
- Vite
- Axios
- Recharts
- React Router DOM

## UI Pages

| Page | Route | Purpose |
|---|---|---|
| Landing | `/` | Product intro and CTA to auth |
| Login | `/login` | Existing user login |
| Signup | `/signup` | New user registration |
| Dashboard | `/dashboard` | User summary + upload history |
| Upload | `/upload` | Upload resume + enter job description |
| Analysis Result | `/analysis/:id` | Resume score, match %, skill gaps, suggestions |

## UI Route Access Rules

- Public routes:
  - `/`
  - `/login`
  - `/signup`
- Protected routes (JWT required):
  - `/dashboard`
  - `/upload`
  - `/analysis/:id`

Auth protection is implemented through `ProtectedRoute`.

## UI Components (Core)

| Component | Role |
|---|---|
| `Navbar` | Top navigation with auth-aware menu |
| `ProtectedRoute` | Guards private routes |
| `ScoreBreakdownChart` | Visual chart for score breakdown |

## UI Data Flow

### Auth Flow

- `AuthContext` stores user + JWT token
- Token saved in `localStorage`
- Axios interceptor injects `Authorization: Bearer <token>`
- Logout clears local session

### Resume + Analysis Flow

1. User uploads `.pdf/.docx` on Upload page.
2. Frontend calls `/api/resume/upload`.
3. Frontend calls `/api/analyze` with uploaded `resume_id` + job text.
4. Navigate to `/analysis/:id`.
5. Fetch full result from `/api/results/:id`.

## UI States and UX Behavior

### Loading States

- Dashboard: history loading state
- Analysis page: result loading state
- Forms: button disabled during submission

### Error States

- Auth errors shown inline
- Upload/analysis errors shown near action button
- Result fetch errors displayed at top of result page

### Empty States

- Dashboard shows "No resumes uploaded yet" when history is empty
- Missing skills section shows "No major skill gaps detected" when list is empty

## Analysis Result UI Layout

The analysis page displays:

- Resume Score (`/100`)
- Match Percentage
- Generated timestamp
- Score Breakdown Chart
- Skills Detected (tag chips)
- Missing Skills (highlight chips)
- Improvement Suggestions (numbered list)

## Visual Design System (Current)

### Color Direction

- Primary dark: `#0f172a`
- Accent: `#0ea5e9`
- Success: `#10b981`
- Warning: `#f59e0b`
- Base background: slate light

### Typography

- Clean sans-serif UI for readability
- Consistent heading hierarchy

### Layout

- Card-based surface design
- Max-width container for content readability
- Table for history and chips for skills

## Responsive Behavior

- Mobile and desktop both supported
- Grid layouts collapse gracefully on small screens
- Forms and cards use full-width responsive patterns

## Frontend Folder Structure

```text
frontend/
|-- src/
|   |-- components/
|   |   |-- Navbar.tsx
|   |   |-- ProtectedRoute.tsx
|   |   `-- ScoreBreakdownChart.tsx
|   |-- pages/
|   |   |-- LandingPage.tsx
|   |   |-- LoginPage.tsx
|   |   |-- SignupPage.tsx
|   |   |-- DashboardPage.tsx
|   |   |-- UploadPage.tsx
|   |   `-- AnalysisResultPage.tsx
|   |-- hooks/
|   |   `-- useAuth.ts
|   |-- services/
|   |   |-- api.ts
|   |   |-- authService.ts
|   |   |-- resumeService.ts
|   |   `-- analysisService.ts
|   |-- store/
|   |   `-- AuthContext.tsx
|   |-- types/
|   |   |-- auth.ts
|   |   |-- resume.ts
|   |   `-- analysis.ts
|   |-- utils/
|   |   `-- format.ts
|   |-- App.tsx
|   |-- main.tsx
|   `-- styles.css
|-- package.json
|-- vite.config.ts
`-- tailwind.config.js
```

## Frontend Setup (PowerShell)

```powershell
cd "d:\AI Resume Analyzer Platform\frontend"
npm install
Copy-Item .env.example .env -Force
npm run dev
```

Frontend URL:
- `http://localhost:5173`

## Full Stack Setup (Docker)

```powershell
cd "d:\AI Resume Analyzer Platform"
docker compose up --build
```

UI URL:
- `http://localhost:3000`

## Frontend API Contract (Used by UI)

| Method | Endpoint | Used In |
|---|---|---|
| POST | `/api/auth/register` | Signup page |
| POST | `/api/auth/login` | Login page |
| POST | `/api/resume/upload` | Upload page |
| GET | `/api/resume/history` | Dashboard page |
| POST | `/api/analyze` | Upload page |
| GET | `/api/results/{id}` | Analysis result page |

## UI Quality Commands

```powershell
cd "d:\AI Resume Analyzer Platform\frontend"
npm run lint
npm run build
```

## Backend Note (For UI Connectivity)

Backend should run at:
- `http://localhost:8000`

Swagger for API testing:
- `http://localhost:8000/docs`

Frontend env value:
- `VITE_API_BASE_URL=http://localhost:8000/api`

---

This README is intentionally UI/frontend-focused and does not include screenshots.
