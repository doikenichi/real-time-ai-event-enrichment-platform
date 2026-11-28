# Guide for Challenge B: the `ServiceStatus` component, one tiny step at a time

Same rules as `guide-a.md`: one idea per step, an example on something *different*, then your turn and a check. Commit at every green step. Open hints one at a time. If you're still stuck, ask Claude or Codex to *"explain step N of guide-b, don't give me the code"*.

Time: about 40–50 minutes the first time.

---

## Step 0: What are we building? (3 min, reading)

The dashboard will show whether each service is OK. Today it gets its first piece: a small **component** that displays one service and its state:

> ingest-api: Healthy

**Words you'll meet**
- **TypeScript** is JavaScript with types: you say what kind of value each thing is, and the compiler (`tsc`) catches mistakes before you run anything.
- **React component:** a function that returns what should appear on screen, written in **JSX** (HTML-like syntax inside TypeScript, in `.tsx` files).
- **Next.js:** the framework the dashboard is built on.
- **Vitest** runs the tests. **Testing Library** renders a component in a fake browser (`jsdom`) and lets tests find things the way a user would: by **role** ("a status message") and **name**.

Open `challenges/day-001/starter/web/dashboard/__tests__/service-status.test.tsx` and read it. Notice:
- `render(<ServiceStatus name="ingest-api" state="ready" />)` draws the component with two **props** (inputs).
- `screen.getByRole("status", { name: "ingest-api" })` finds the element whose role is `status` and whose accessible name is `ingest-api`.
- `.textContent).toContain("Healthy")` checks the visible text.

---

## Step 1: Create the dashboard and see red (10 min)

Run from the repo root:
```bash
printf 'packages:\n  - "web/*"\n' > pnpm-workspace.yaml
pnpm create next-app@latest web/dashboard --ts --app --eslint --use-pnpm --no-tailwind --no-src-dir --import-alias "@/*" --yes
cd web/dashboard
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths
cp -r ../../challenges/day-001/starter/web/dashboard/__tests__ .
```
- `pnpm-workspace.yaml` is the TypeScript side's workspace file: every folder in `web/` is a project.
- `create next-app` generates a working Next.js app.
- `pnpm add -D` adds **dev dependencies** (tools needed only to develop and test).

Create `web/dashboard/vitest.config.mts` with this content (it's setup, not part of the challenge, so here it is in full):
```ts
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: "jsdom", // a fake browser, so components can render
    globals: true,        // lets Testing Library clean up the page between tests
  },
});
```
In `web/dashboard/package.json`, inside `"scripts"`, add `"test": "vitest"`.

```bash
pnpm test --run
```
**Expected:** an error like `Failed to resolve import "../components/service-status"`. That's the right red: the component doesn't exist yet.

**Commit:** `day-001: failing tests for service status`

---

## Step 2: A component that exists (5 min)

**Idea: a component is a function** that takes props and returns JSX. `export` makes it importable from other files.

**Example (a different component):**
```tsx
// components/greeting.tsx
type GreetingProps = { name: string };

export function Greeting({ name }: GreetingProps) {
  return <p>Hello {name}</p>;
}
```
- `type GreetingProps = { name: string }` describes the props: one prop, `name`, which is a string.
- `{ name }: GreetingProps` takes the `name` prop out of the props object (this is called **destructuring**).
- `{name}` inside JSX inserts the value into the page.

**Your turn:** create `web/dashboard/components/service-status.tsx` that exports `ServiceStatus`, taking `name` and `state` props (both `string` for now) and showing them in a `<p>`.

**Check:** `pnpm test --run`. **Expected:** the import works; both tests now fail because no element has the role `status`. A different red means progress.

---

## Step 3: Make it findable by role and name (5 min)

**Idea: accessibility roles.** Screen readers announce elements by their **role** and **accessible name**. `role="status"` means "a message about the current state" (screen readers read it politely when it changes). `aria-label` gives the element its name.

**Example:**
```tsx
<p role="alert" aria-label="Upload">Upload failed</p>
```

**Your turn:** give your element `role="status"`, and set its accessible name to the service name.

**Check:** the tests still fail, but now with a message about the text (it doesn't contain "Healthy"). Progress.

---

## Step 4: Green: turn a state into a label (10 min)

**Idea: a union type** lists the only values allowed: `type Size = "small" | "large"`. Passing `"medium"` becomes a compile error.

**Idea: a `Record`** maps every value of a type to something. Combined with a union, the compiler *forces* you to handle every state: forget one and `tsc` complains.

**Example:**
```tsx
type Size = "small" | "large";

const SIZE_LABELS: Record<Size, string> = {
  small: "S",
  large: "L",
};

export function SizeTag({ size }: { size: Size }) {
  return <span>{SIZE_LABELS[size]}</span>;
}
```

**Your turn:**
1. Make a type `ServiceState` with the two states the tests use, `"ready"` and `"unavailable"`.
2. Map them to the labels the tests expect.
3. Change the `state` prop from `string` to `ServiceState`, and show the label.

**Check:** `pnpm test --run` → **2 passed**. Green!

**Commit:** `day-001: service status shows healthy or unavailable`

---

## Step 5: Your own red → green for "unknown" (10 min)

Before the first readiness answer arrives, the dashboard doesn't know the state. It must say so in words, not just with a grey colour (WCAG 2.2, 1.4.1: colour can't be the only signal).

1. **Spec:** open `openspec/changes/add-dashboard-service-status/specs/dashboard-status/spec.md`. Copy the shape of an existing scenario, and add *"shows the state as unknown before the first result"*, with the exact words it shows (for example "Checking…" or "Unknown"). Run `openspec validate add-dashboard-service-status --strict`.
2. **Red:** in the test file, copy one test and change it for `state="unknown"` and your words. Run it: it fails. TypeScript may also complain that `"unknown"` isn't a `ServiceState`. That's the compiler protecting you.
3. **Commit:** `day-001: failing test for unknown service state`
4. **Green:** add `"unknown"` to the union. `tsc` then tells you the `Record` is missing a label. Add it.
5. **Check:** **3 passed**. **Commit:** `day-001: service status shows unknown`

---

## Step 6: Show it on the page, then quality checks (7 min)

1. Open `app/page.tsx`. Import your component (`import { ServiceStatus } from "@/components/service-status";`), and render it for `ingest-api` with the state written in by hand for now.
2. Run `pnpm dev`, open the forwarded port 3000 in the browser, and look at it. Stop it with Ctrl+C.
3. Quality checks:

| Command | What it checks |
|---|---|
| `pnpm test --run` | the tests |
| `pnpm exec tsc --noEmit` | the types, without building anything |
| `pnpm lint` | common mistakes and React rules |

**Commit:** `day-001: dashboard shows ingest-api status`

Then do the Docs step from the README (`web/dashboard/README.md`).

---

## Glossary
| Term | Meaning |
|---|---|
| **component** | a function that returns part of the page |
| **props** | a component's inputs |
| **JSX / TSX** | HTML-like syntax inside JavaScript or TypeScript files |
| **union type** | a type that allows only listed values |
| **`Record<K, V>`** | an object with one `V` for every key in `K` |
| **role, accessible name** | how assistive technology identifies an element |
| **jsdom** | a fake browser for tests |
| **dev dependency** | a package needed only to develop or test |

## Learn more (optional, short)
- [TypeScript for JavaScript programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)
- React: [Your first component](https://react.dev/learn/your-first-component) and [Passing props](https://react.dev/learn/passing-props-to-a-component)
- Testing Library: [Which query should I use?](https://testing-library.com/docs/queries/about/#priority)
- Node.js Design Patterns (4th ed.): the module system chapter, for how `import` and `export` work
