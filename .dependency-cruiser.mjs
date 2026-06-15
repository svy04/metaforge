export default {
  forbidden: [
    {
      name: 'no-circular',
      severity: 'error',
      from: {},
      to: {
        circular: true,
      },
    },
    {
      name: 'not-to-unresolvable',
      severity: 'error',
      from: {},
      to: {
        couldNotResolve: true,
      },
    },
    {
      name: 'not-src-to-scripts',
      severity: 'error',
      from: {
        path: '^src/',
      },
      to: {
        path: '^scripts/',
      },
    },
  ],
  options: {
    doNotFollow: {
      path: 'node_modules',
      dependencyTypes: [
        'npm',
        'npm-dev',
        'npm-optional',
        'npm-peer',
        'npm-bundled',
        'npm-no-pkg',
      ],
    },
  },
}
