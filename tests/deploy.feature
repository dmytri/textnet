Feature: BDA | Saleor Commerce Platform on Alpine Linux

  @dev
  SCA Scenario: Target a development environment for testing
     SCA1 When target environment is configured for development
     SCA2 Then the system is configured for development testing

  @ci
  SCB Scenario: Target a CI environment for verification
     SCB1 When target environment is configured for continuous integration
     SCB2 Then the system is configured for CI testing

  @prod
  SCC Scenario: Target a production environment for customers
     SCC1 When target environment is configured for production
     SCC2 Then the system is configured for production use

  @dev @ci @prod
  SCD Scenario: Provide a stable Alpine Linux platform
     SCD1 When system packages up to date
     SCD2 Then OS Alpine Linux 3.21

  @dev @ci @prod
  SCE Scenario: Enable required runtime environments for Saleor
     SCE1 When Python runtime is available
     SCE2 And NodeJS runtime is available
     SCE3 And SQLite database is available
     SCE4 And Poetry is available
     SCE5 Then python version >= 3.12
     SCE6 And nodejs version >= 18
     SCE7 And sqlite version >= 3.48
     SCE8 And poetry version >= 1.8

  @dev @ci @prod
  SCF Scenario: Provide Saleor commerce capabilities
     SCF1 When build dependencies are available
     SCF2 And Saleor source code is available
     SCF3 And Saleor Python components are installed
     SCF4 And Saleor service definition is present
     SCF5 And Saleor service is enabled
     SCF6 Then saleor version >= 3.20
     SCF7 And OpenRC manages the running saleor service
     SCF8 And Saleor GraphQL endpoint responds successfully
