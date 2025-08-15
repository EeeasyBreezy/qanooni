import { testFixture as test, expect } from './msw.fixtures';

test('Upload page controls are visible', async ({ uploadPage }) => {
  await uploadPage.goto();
  await expect(uploadPage.page.getByText('Drag and drop PDF/DOCX files here, or click to select')).toBeVisible();
  await expect(uploadPage.table).toBeVisible();
});


