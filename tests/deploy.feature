Feature: BDA | Saleor Commerce Platform on Alpine Linux

  @dev
  Scenario: Target a development environment for testing
     When set target environment to dev
     Then the system is configured for development testing

  @ci
  Scenario: Target a CI environment for verification
     When set target environment to ci
     Then the system is configured for continuous integration

  @prod
  Scenario: Target a production environment for customers
     When set target environment to prod
     Then the system is configured for production use

  @dev @ci @prod
  Scenario: Provide a stable Alpine Linux platform
     When system packages up to date
     Then OS Alpine Linux 3.21
      And the platform is ready for application hosting

  @dev @ci @prod
  Scenario: Enable required runtime environments for Saleor
     When Python runtime is available
      And NodeJS runtime is available
      And SQLite database is available
     Then python version >= 3.12
      And nodejs version >= 18
      And sqlite version >= 3.48.0
      And the platform can run Saleor components

  @dev @ci @prod
  Scenario: Provide Saleor commerce capabilities
     Given Saleor dependencies are installed
     When Saleor core is available
     Then saleor version >= 3.20
      And saleor service is running
      And Saleor commerce platform is operational
