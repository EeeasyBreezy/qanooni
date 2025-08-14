export const searchQueryKeyFactory = {
  all: ['search'] as const,
  byQuestion: (q: string) => ['search', q] as const,
};


