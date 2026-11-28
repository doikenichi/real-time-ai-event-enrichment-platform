#!/usr/bin/env bash
# Day 001 · Challenge B setup: creates the Next.js dashboard with Vitest and Testing Library,
# and copies in the failing tests. Setup isn't the lesson, so it's scripted.
# Run from the repo root, inside the dev container:  bash challenges/day-001/setup-b.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ ! -f pnpm-workspace.yaml ]; then
  printf 'packages:\n  - "web/*"\n' > pnpm-workspace.yaml
fi

if [ ! -d web/dashboard ]; then
  pnpm create next-app@latest web/dashboard --ts --app --eslint --use-pnpm \
    --no-tailwind --no-src-dir --import-alias "@/*" --yes
fi

cd web/dashboard
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths
pnpm pkg set scripts.test=vitest

cat > vitest.config.mts <<'TS'
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: "jsdom", // a fake browser, so components can render
    globals: true, // lets Testing Library clean up the page between tests
  },
});
TS

mkdir -p __tests__ lib
cp ../../challenges/day-001/starter/web/dashboard/__tests__/service-status.test.tsx __tests__/
cp ../../challenges/day-001/starter/web/dashboard/lib/service-state.test.ts lib/   # drill B

cd ../..
echo
echo "Setup done. Start with drill B (challenges/day-001/drill-b.md), then run:  lab test b"
echo "Expected: an error that '../components/service-status' can't be found (that's red)."
echo 'Then commit it:       lab save "failing tests for service status"'
