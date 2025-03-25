Feature: BDA | Saleor Commerce Platform on Alpine Linux

  @dev
  Scenario: Target a development environment for testing  # SCA
     When target environment is configured for development  # SCA1
     Then the system is configured for development testing  # SCA2

  @ci
  Scenario: Target a CI environment for verification  # SCB
     When target environment is configured for continuous integration  # SCB1
     Then the system is configured for CI testing  # SCB2

  @prod
  Scenario: Target a production environment for customers  # SCC
     When target environment is configured for production  # SCC1
     Then the system is configured for production use  # SCC2

  @dev @ci @prod
  Scenario: Provide a stable Alpine Linux platform  # SCD
     When system packages up to date  # SCD1
     Then OS Alpine Linux 3.21  # SCD2

  @dev @ci @prod
  Scenario: Enable required runtime environments for Saleor  # SCE
     When Python runtime is available  # SCE1
      And NodeJS runtime is available  # SCE2
      And SQLite database is available  # SCE3
      And Poetry is available  # SCE4
     Then python version >= 3.12  # SCE5
      And nodejs version >= 18  # SCE6
      And sqlite version >= 3.48  # SCE7
      And poetry version >= 1.8  # SCE8

  @dev @ci @prod
  Scenario: Provide Saleor commerce capabilities  # SCF
     When build dependencies are available  # SCF1
      And Saleor source code is available  # SCF2
      And Saleor Python components are installed  # SCF3
      And Saleor service definition is present  # SCF4
      And Saleor service is enabled  # SCF5
     Then saleor version >= 3.20  # SCF6
      And OpenRC manages the running saleor service  # SCF7
      And Saleor GraphQL endpoint responds successfully  # SCF8
