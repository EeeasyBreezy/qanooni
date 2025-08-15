import { Page, Locator, expect } from '@playwright/test';

export class QueryPagePOM {
  readonly page: Page;
  readonly questionTextarea: Locator;
  readonly sendButton: Locator;
  readonly clearButton: Locator;
  readonly resultsGrid: Locator;

  constructor(page: Page) {
    this.page = page;
    this.questionTextarea = page.getByTestId('query-input');
    this.sendButton = page.getByRole('button', { name: 'Send' });
    this.clearButton = page.getByRole('button', { name: 'Clear' });
    this.resultsGrid = page.getByTestId('query-results');
  }

  async goto() {
    await this.page.goto('/search');
  }

  async ask(question: string) {
    await this.questionTextarea.fill(question);
    await expect(this.sendButton).toBeEnabled();
    await this.sendButton.click();
  }
}

export default QueryPagePOM;


