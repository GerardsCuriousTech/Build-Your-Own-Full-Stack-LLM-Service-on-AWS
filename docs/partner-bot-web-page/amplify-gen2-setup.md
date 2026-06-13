# Amplify Gen 2 Setup

## Goal

Scaffold a React application with Vite, initialize an Amplify Gen 2 backend, and deploy a cloud sandbox you can develop against. When finished you will have a running local dev server connected to a live Amplify sandbox environment.

## Contract

This page produces no Lambda interaction. The deliverable is a working project structure:

```
partner-bot/
├── amplify/
│   ├── backend.ts
│   └── ...
├── src/
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

Amplify Gen 2 generates an `amplify_outputs.json` at the project root when you deploy a sandbox. Your React app imports this file to discover backend endpoints at runtime.

## Required Reading

Read these pages before you begin — the exercise assumes familiarity with the concepts they cover.

- Amplify Gen 2 getting started: <https://docs.amplify.aws/react/start/quickstart/>
- Vite React guide: <https://vite.dev/guide/>
- Amplify Gen 2 sandbox environments: <https://docs.amplify.aws/react/deploy-and-host/sandbox-environments/setup/>

## Constraints

1. Use **Vite** as the build tool. Do not use any other React scaffolding tool.
2. Use **TypeScript** for both the React app and the Amplify backend definition.
3. The Amplify backend must target the **Gen 2** resource model (`amplify/backend.ts`, `defineBackend`). Do not use the Gen 1 CLI (`amplify init`).
4. Deploy a personal **sandbox** environment (`npx ampx sandbox`) rather than a shared branch environment during development.
5. Add `amplify_outputs.json` and `node_modules/` to `.gitignore` — these are generated artifacts that must not be committed.

## Acceptance Criteria

- [ ] `npm run dev` starts a Vite dev server on `localhost:5173` and renders a default page.
- [ ] `amplify/backend.ts` exists and exports a valid backend definition (even if it defines no resources yet).
- [ ] Running `npx ampx sandbox` deploys without errors and produces `amplify_outputs.json`.
- [ ] The React app loads `amplify_outputs.json` via `Amplify.configure()` at startup without console errors.
- [ ] `.gitignore` excludes `amplify_outputs.json` and `node_modules/`.

## Hints

<details>
<summary>Scaffolding the project</summary>

`npm create vite@latest partner-bot -- --template react-ts` generates the Vite + React + TypeScript starter. From inside that directory, `npm create amplify@latest` initializes the Gen 2 backend structure.

</details>

<details>
<summary>Configuring Amplify in the app entry point</summary>

In `src/main.tsx`, import the generated outputs and call `Amplify.configure()` before rendering the root component:

```tsx
import outputs from "../amplify_outputs.json";
import { Amplify } from "aws-amplify";

Amplify.configure(outputs);
```

Vite resolves JSON imports natively — no loader config needed.

</details>

<details>
<summary>Sandbox lifecycle</summary>

`npx ampx sandbox` watches your `amplify/` directory for changes and hot-deploys them. Press `Ctrl+C` to stop watching; the sandbox resources remain deployed. Run `npx ampx sandbox delete` when you want to tear them down.

</details>
