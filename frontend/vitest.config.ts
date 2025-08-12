import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    exclude: [
      'node_modules',
      'dist',
      '.{idea,git,cache,output,temp}/**',
      'integration-tests/**',
      'tests-examples/**',
    ],
    environment: 'node',
  },
})


