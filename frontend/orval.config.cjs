module.exports = {
    fastapi: {
      input: 'http://localhost:8000/docs',
      output: {
        mode: 'single',
        target: 'src/shared/api/generated.ts',
        schemas: 'src/shared/api/schemas',
        client: 'axios',
        prettier: true,
      },
      hooks: {
        afterAllFilesWrite: 'eslint --fix src/api || true',
      },
    },
  };