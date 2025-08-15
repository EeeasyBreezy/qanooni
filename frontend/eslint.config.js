import globals from 'globals';
import parser from '@typescript-eslint/parser';
import reactPlugin from 'eslint-plugin-react';
import prettierPlugin from 'eslint-plugin-prettier';
import typescriptPlugin from '@typescript-eslint/eslint-plugin';
import importPlugin from 'eslint-plugin-import';
import reactHooksPlugin from 'eslint-plugin-react-hooks';

import archPlugin from './eslint-rules/arch-rules-plugin/index.js';

const sanitizedGlobals = Object.keys(globals)
  .filter((key) => key.trim() === key)
  .reduce((acc, key) => {
    acc[key] = 'readonly';
    return acc;
  }, {});

export default [
  reactPlugin.configs.flat.recommended,
  {
    files: ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx', '**/*.cjs'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser,
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
      globals: {
        ...sanitizedGlobals,
      },
    },
    plugins: {
      react: reactPlugin,
      prettier: prettierPlugin,
      '@typescript-eslint': typescriptPlugin,
      import: importPlugin,
      'react-hooks': reactHooksPlugin,
      archPlugin,
    },
    rules: {
      'archPlugin/no-banned-imports': 'off',
      'import/order': [
        'warn',
        {
          groups: [[ 'builtin', 'external' ], 'internal', [ 'sibling', 'parent', 'index' ]],
          'newlines-between': 'always',
        },
      ],
      'no-restricted-syntax': [
        'warn',
        {
          selector: "CallExpression[callee.property.name='goto']",
          message: 'Using of `.goto()` is restricted, use visit methods instead.',
        },
        {
          selector: "CallExpression[callee.property.name='reload']",
          message: 'Using of `.reload()` is restricted, use visit methods instead.',
        },
      ],
      '@typescript-eslint/no-explicit-any': ['warn'],
      'prettier/prettier': [
        'error',
        {
          trailingComma: 'es5',
        },
      ],
      'import/extensions': [
        'error',
        'ignorePackages',
        {
          ts: 'never',
          tsx: 'never',
        },
      ],
      'no-console': ['error', { allow: ['error', 'info'] }],
      'no-debugger': 'error',
      '@typescript-eslint/consistent-type-imports': 'error',
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          varsIgnorePattern: 'Schema$|^_$',
          argsIgnorePattern: 'Schema$|^_$',
        },
      ],
      'react/react-in-jsx-scope': 'off',
      'react/display-name': 'off',
      'react/no-unescaped-entities': 'warn',
      'react-hooks/exhaustive-deps': 'warn',
      'react-hooks/rules-of-hooks': 'warn',
      radix: 'warn',
    },
    settings: {
      react: {
        version: 'detect',
      },
      'import/resolver': {
        node: {
          extensions: ['.js', '.jsx', '.ts', '.tsx'],
        },
        typescript: {
          alwaysTryTypes: true,
          project: './tsconfig.json',
        },
      },
    },
    ignores: ['node_modules/', 'dist/', 'public/', 'coverage/'],
  },
  {
    files: ['**/e2e/**/*.test.ts', '**/Page.model.ts', '**/auth.setup.ts'],
    rules: {
      'no-restricted-syntax': ['off'],
    },
  },
];

