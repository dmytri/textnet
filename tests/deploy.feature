Feature: SC Saleor Commerce Platform on Alpine Linux | BDA

  @dev
  Scenario: SCA Target a development environment for testing
     When SCA1 target environment is configured for development
     Then SCA2 the system is configured for development testing

  @ci
  Scenario: SCB Target a CI environment for verification
     When SCB1 target environment is configured for continuous integration
     Then SCB2 the system is configured for CI testing

  @prod
  Scenario: SCC Target a production environment for customers
     When SCC1 target environment is configured for production
     Then SCC2 the system is configured for production use

  @dev @ci @prod
  Scenario: SCD Provide a stable Alpine Linux platform
     When SCD1 system packages up to date
     Then SCD2 OS Alpine Linux 3.21

  @dev @ci @prod
  Scenario: SCE Enable required runtime environments for Saleor
     When SCE1 Python runtime is available
      And SCE2 NodeJS runtime is available
      And SCE3 SQLite database is available
      And SCE4 Poetry is available
     Then SCE5 python version >= 3.12
      And SCE6 nodejs version >= 18
      And SCE7 sqlite version >= 3.48
      And SCE8 poetry version >= 1.8

  @dev @ci @prod
  Scenario: SCF Provide Saleor commerce capabilities
     When SCF1 build tools are available
     When SCF2 Saleor source code is available
     When SCF3 Saleor Python virtual environment is available
     When SCF4 Saleor Python dependencies are installed
     When SCF5 Saleor service definition is present
     When SCF6 Saleor service is enabled
     Then SCF7 saleor version >= 3.20
      And SCF7 OpenRC manages the running saleor service
      And SCF8 Saleor GraphQL endpoint responds successfully
