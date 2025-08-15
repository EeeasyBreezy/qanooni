import { Page, Locator } from '@playwright/test';

export class UploadPagePOM {
  readonly page: Page;
  readonly fileInput: Locator;
  readonly table: Locator;

  constructor(page: Page) {
    this.page = page;
    this.fileInput = page.getByTestId('upload-dropzone');
    this.table = page.getByTestId('upload-table');
  }

  async goto() {
    await this.page.goto('/upload');
  }

  async addFiles(paths: string | string[]) {
    await this.fileInput.setInputFiles(paths);
  }

  uploadButtonFor(filename: string): Locator {
    return this.page.getByRole('button', { name: `Upload ${filename}` });
  }

  tableRows(): Locator {
    return this.table.locator('tbody > tr');
  }
}

export default UploadPagePOM;


