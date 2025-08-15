import { Page, Locator } from '@playwright/test';

export class DashboardPagePOM {
  readonly page: Page;
  readonly agreementsChart: Locator;
  readonly governingLawChart: Locator;
  readonly industriesTable: Locator;

  constructor(page: Page) {
    this.page = page;
    this.agreementsChart = page.getByTestId('agreements-chart');
    this.governingLawChart = page.getByTestId('governing-law-chart');
    this.industriesTable = page.getByTestId('industries-table');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  countHeader(): Locator {
    return this.page.getByRole('columnheader', { name: 'Count' });
  }

  tableRows(): Locator {
    return this.industriesTable.locator('.MuiDataGrid-row');
  }
}

export default DashboardPagePOM;


