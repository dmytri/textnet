Feature: BDA | Saleor Commerce Platform on Alpine Linux

  @dev
  Scenario: Target a development environment for testing
     When target environment is configured for development
     Then the system is configured for development testing

  @ci
  Scenario: Target a CI environment for verification
     When target environment is configured for continuous integration
     Then the system is configured for CI testing

  @prod
  Scenario: Target a production environment for customers
     When target environment is configured for production
     Then the system is configured for production use

  @dev @ci @prod
  Scenario: Provide a stable Alpine Linux platform
     When system packages up to date
     Then OS Alpine Linux 3.21

  @dev @ci @prod
  Scenario: Enable required runtime environments for Saleor
     When Python runtime is available
      And NodeJS runtime is available
      And SQLite database is available
      And pipx is available
      And Poetry is available
     Then python version >= 3.12
      And nodejs version >= 18
      And sqlite version >= 3.48.0
      And pipx version >= 1.7.1
      And poetry version >= 1.8

  @skip @dev @ci @prod
  Scenario: Provide Saleor commerce capabilities
     Given Saleor dependencies are installed
     When build dependencies are available
      And Saleor source code is available
      And Saleor Python components are installed
      And Saleor service definition is present
      And Saleor service is enabled
     Then saleor version >= 3.20
      And saleor service is running
      And Saleor commerce platform is operational
