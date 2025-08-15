import { test as base } from '@playwright/test';
import UploadPagePOM from './pom/UploadPagePOM';
import DashboardPagePOM from './pom/DashboardPagePOM';
import QueryPagePOM from './pom/QueryPagePOM';

// Expose a per-test MSW mode switch via localStorage flags the app reads at boot.
type MswFixtures = {
  setMswMode: (mode: 'success' | 'error' | 'loading') => Promise<void>;
};

type PomFixtures = {
  uploadPage: UploadPagePOM;
  dashboardPage: DashboardPagePOM;
  queryPage: QueryPagePOM;
};


export const testFixture = base.extend<MswFixtures & PomFixtures>({
  setMswMode: async ({ page }, use) => {
    await use(async (mode) => {
      await page.addInitScript((m) => {
        localStorage.setItem('msw:mode', m);
      }, mode);
    });
  },
  uploadPage: async ({ page }, use) => {
    await use(new UploadPagePOM(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPagePOM(page));
  },
  queryPage: async ({ page }, use) => {
    await use(new QueryPagePOM(page));
  },
});

export { expect } from '@playwright/test';


