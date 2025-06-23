# Detailed Frontend Development Plan (Next.js + Tailwind CSS)

This plan outlines the steps for developing the frontend of the portfolio website using Next.js and Tailwind CSS, focusing on integration with the existing Django backend.

## 1. Project Initialization and Setup

*   **Initialize Next.js Project:** Create a new Next.js project within the `portfolio_project/frontend` directory.
    ```bash
    npx create-next-app@latest portfolio_project/frontend --ts --tailwind --eslint --app --src-dir --use-pnpm
    ```
    *(Note: `--use-pnpm` is optional, adjust based on preferred package manager)*
*   **Configure Tailwind CSS:** Ensure Tailwind CSS is correctly set up and integrated with Next.js. This is typically handled by `create-next-app` when `--tailwind` is specified.
*   **Set up Basic Folder Structure:** Organize the `src` directory with initial folders for components, pages, and utilities as outlined in the proposed file structure.

## 2. Core Layout and Navigation

*   **Create `Layout` Component:** Develop a `Layout` component (e.g., `src/components/Layout.tsx`) that wraps the main content of the application. This component will include:
    *   A `Header` component with navigation links (Home, Achievements, Digital Products, Login/Signup/Dashboard).
    *   A `Footer` component for copyright or other general information.
*   **Implement Responsive Navigation:** Ensure the navigation menu is responsive and adapts well to different screen sizes (e.g., using a hamburger menu on mobile).

## 3. Authentication Pages and Flow

*   **Create Login Page:** Develop `src/app/login/page.tsx` with a form for user login.
*   **Create Signup Page:** Develop `src/app/signup/page.tsx` with a form for user registration.
*   **Client-Side Form Validation:** Implement robust client-side validation for both login and signup forms to provide immediate feedback to the user.
*   **Authentication State Management:** Set up a global state management solution (e.g., React Context API, Zustand, or Redux Toolkit) to manage the user's authentication status and store the JWT token.
*   **Secure JWT Token Storage:** Implement a strategy to securely store the JWT token. `httpOnly` cookies are recommended if the Django backend is configured to issue them. If not, local storage can be used with careful consideration of XSS vulnerabilities.
*   **API Utility for Authentication:** Create a utility file (e.g., `src/utils/api.ts`) that configures an Axios instance or similar for making API requests. This utility will automatically include the JWT token in the headers for authenticated requests.

## 4. Protected Routes and Dashboard

*   **Create Dashboard Page:** Develop `src/app/dashboard/page.tsx` as a protected route accessible only to logged-in users. This page will serve as the user's personal area.
*   **Implement Route Protection:** Create a higher-order component (HOC) or a custom hook (e.g., `src/hooks/useAuth.ts`) to wrap pages that require authentication. This will check the user's authentication status and redirect unauthenticated users to the login page.

## 5. Content Pages

*   **Home Page (`src/app/page.tsx`):**
    *   Display a summary of the trader's profile.
    *   Show key statistics or highlights.
    *   Include a prominent call-to-action (e.g., "View Achievements" or "Explore Products").
*   **Achievements Page (`src/app/achievements/page.tsx`):**
    *   Fetch and display the list of achievements from the Django API.
    *   Present achievements in a clear, organized manner (e.g., using cards or a list).
*   **Digital Products Page (`src/app/products/page.tsx`):**
    *   List available digital products, fetching data from the Django API.
    *   Include "purchase" or "download" buttons (future-proof for payment integration).
*   **About Page (`src/app/about/page.tsx`):** Provide information about the trader.
*   **Contact Page (`src/app/contact/page.tsx`):** Include a contact form or contact details.

## 6. Data Fetching and Caching

*   **Integrate SWR or React Query:** Utilize a data fetching library like SWR or React Query for efficient data fetching, caching, revalidation, and error handling for all API calls (e.g., achievements, products, user data).

## 7. UI/UX Enhancements

*   **Tailwind CSS Styling:** Apply Tailwind CSS classes consistently across all components and pages to achieve a modern and cohesive design.
*   **Responsiveness:** Ensure the entire website is fully responsive and provides an optimal viewing experience across various devices (desktops, tablets, mobile phones).
*   **User Feedback:** Implement clear success and error message displays for all API actions (e.g., using toast notifications, inline messages, or modal dialogs).

## 8. Environment Variables

*   **Configure API Endpoint:** Set up environment variables (e.g., in a `.env.local` file) to store the Django backend API endpoint URL. This allows for easy switching between local development and production environments.

## 9. Testing and Integration

*   **Manual Testing:** Thoroughly test all pages, forms, and authentication flows manually.
*   **API Call Verification:** Verify that all frontend API calls successfully interact with the Django backend for authentication, fetching achievements, and listing products.
*   **Local Development Focus:** Ensure the setup is optimized for local development, considering the backend is also running locally.

## Frontend File Structure (Proposed):

```
portfolio_project/
└── frontend/
    ├── public/
    │   └── ... (static assets like images, favicons)
    ├── src/
    │   ├── app/ (Next.js 13+ App Router structure)
    │   │   ├── layout.tsx (Root layout for the application)
    │   │   ├── page.tsx (Home page)
    │   │   ├── login/
    │   │   │   └── page.tsx (Login page)
    │   │   ├── signup/
    │   │   │   └── page.tsx (Signup page)
    │   │   ├── dashboard/
    │   │   │   └── page.tsx (Protected dashboard page)
    │   │   ├── achievements/
    │   │   │   └── page.tsx (Achievements listing page)
    │   │   ├── products/
    │   │   │   └── page.tsx (Digital products listing page)
    │   │   ├── about/
    │   │   │   └── page.tsx (About page)
    │   │   └── contact/
    │   │       └── page.tsx (Contact page)
    │   ├── components/
    │   │   ├── Layout.tsx
    │   │   ├── Header.tsx
    │   │   ├── Footer.tsx
    │   │   ├── AuthForm.tsx (Reusable component for login/signup forms)
    │   │   ├── AchievementCard.tsx
    │   │   ├── ProductCard.tsx
    │   │   └── UI/ (e.g., Button, Input, LoadingSpinner - for generic UI elements)
    │   ├── hooks/
    │   │   └── useAuth.ts (Custom hook for authentication logic and route protection)
    │   ├── context/ (or store/ if using a dedicated state management library)
    │   │   └── AuthContext.tsx (React Context for authentication state)
    │   ├── utils/
    │   │   ├── api.ts (Axios instance or fetch wrapper for API calls, handles token)
    │   │   └── validation.ts (Utility functions for form validation)
    │   ├── styles/
    │   │   └── globals.css (Main CSS file, imports Tailwind directives)
    │   └── types/
    │       └── index.ts (TypeScript interfaces for data models like User, Achievement, Product)
    ├── .env.local (Environment variables for local development)
    ├── next.config.js (Next.js configuration)
    ├── package.json (Project dependencies and scripts)
    ├── postcss.config.js (PostCSS configuration for Tailwind CSS)
    ├── tailwind.config.js (Tailwind CSS configuration)
    └── tsconfig.json (TypeScript configuration)
```

## Mermaid Diagram: Frontend Architecture Overview

```mermaid
graph TD
    A[User] --> B(Browser)
    B --> C{Next.js Frontend}

    C --> D[Pages]
    D --> D1(Home)
    D --> D2(Login)
    D --> D3(Signup)
    D --> D4(Achievements)
    D --> D5(Products)
    D --> D6(Dashboard - Protected)
    D --> D7(About)
    D --> D8(Contact)

    C --> E[Components]
    E --> E1(Layout)
    E --> E2(Header)
    E3(Footer)
    E4(Auth Forms)
    E5(Achievement Cards)
    E6(Product Cards)

    C --> F[Authentication Flow]
    F --> F1(Login/Signup Forms)
    F --> F2(JWT Token Storage - httpOnly cookies)
    F --> F3(Auth Context/State)
    F --> F4(Route Protection)

    C --> G[Data Fetching]
    G --> G1(SWR/React Query)
    G --> G2(API Utility)

    G2 --> H[Django Backend API]
    H --> H1(Auth Endpoints)
    H --> H2(Achievements Endpoints)
    H --> H3(Products Endpoints)

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#dfd,stroke:#333,stroke-width:2px
    style E fill:#ffd,stroke:#333,stroke-width:2px
    style F fill:#fdd,stroke:#333,stroke-width:2px
    style G fill:#ddf,stroke:#333,stroke-width:2px
    style H fill:#cfc,stroke:#333,stroke-width:2px