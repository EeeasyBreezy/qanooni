import { describe, it, expect } from 'vitest';
import { mapDashboardStatsDtoToModel } from './dashboardStatsMapper';

describe('dashboardStatsMapper', () => {
  it('maps DTO snake_case to model camelCase', () => {
    const dto = {
      agreement_types: { NDA: 4, MSA: 3 },
      jurisdictions: { UAE: 5, UK: 2 },
      industries: { Technology: 3, 'Oil & Gas': 4 },
    };

    const model = mapDashboardStatsDtoToModel(dto);

    expect(model.agreementTypes).toEqual({ NDA: 4, MSA: 3 });
    expect(model.jurisdictions).toEqual({ UAE: 5, UK: 2 });
    expect(model.industries).toEqual({ Technology: 3, 'Oil & Gas': 4 });
  });
});


