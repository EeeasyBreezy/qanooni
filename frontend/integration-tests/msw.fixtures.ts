import { test as base } from '@playwright/test';

// Expose a per-test MSW mode switch via localStorage flags the app reads at boot.
type MswFixtures = {
  setMswMode: (mode: 'success' | 'error' | 'loading') => Promise<void>;
};

export const test = base.extend<MswFixtures>({
  setMswMode: async ({ page }, use) => {
    await use(async (mode) => {
      await page.addInitScript((m) => {
        localStorage.setItem('msw:mode', m);
      }, mode);
    });
  },
});

export { expect } from '@playwright/test';


