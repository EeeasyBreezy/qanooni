import { testFixture as test, expect } from './msw.fixtures';

test('Query page controls are visible', async ({ queryPage }) => {
  await queryPage.goto();
  await expect(queryPage.questionTextarea).toBeVisible();
  await expect(queryPage.sendButton).toBeVisible();
  await expect(queryPage.clearButton).toBeVisible();
});


