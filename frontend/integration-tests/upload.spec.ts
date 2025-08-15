import { testFixture as test, expect } from './msw.fixtures';

test('Upload page controls are visible', async ({ uploadPage }) => {
  await uploadPage.goto();
  await expect(uploadPage.fileInput).toBeVisible();
  await expect(uploadPage.table).toBeVisible();
});


