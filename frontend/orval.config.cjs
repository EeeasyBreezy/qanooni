module.exports = {
    fastapi: {
      input: 'http://localhost:8000/openapi.json',
      output: {
        mode: 'single',
        target: 'src/shared/api/generated.ts',
        schemas: 'src/shared/api/types',
        client: 'axios',
        prettier: true,
      },
    },
  };