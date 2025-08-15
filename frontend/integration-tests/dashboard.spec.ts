import { testFixture as test, expect } from './msw.fixtures';

test('Dashboard page controls are visible', async ({ dashboardPage }) => {
  await dashboardPage.goto();
  await expect(dashboardPage.agreementsChart).toBeVisible();
  await expect(dashboardPage.governingLawChart).toBeVisible();
  await expect(dashboardPage.industriesTable).toBeVisible();
});


