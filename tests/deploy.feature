Feature: TN TextNet Saleor Commerce Based Platform on Alpine Linux | BDA

  @dev
  Scenario: TND Target a development environment for testing
     When TNDE the target environment is configured for development
     Then TNDC the system is configured for development testing

  @ci
  Scenario: TNC Target a CI environment for verification
     When TNCE the target environment is configured for continuous integration
     Then TNCC the system is configured for CI testing

  @prod
  Scenario: TNP Target a production environment for customers
     When TNPE the target environment is configured for production
     Then TNPC the system is configured for production use

  @dev @ci @prod
  Scenario: TNA Provide a stable Alpine Linux platform
     When TNAU the system packages up to date
     Then TNAA OS Alpine Linux 3.21

  @dev @ci @prod
  Scenario: TNR Enable required runtime environments for Saleor
     When TNRA Python runtime is available
      And TNRB NodeJS runtime is available
      And TNRC PostgreSQL database is available
      And TNRS PostgreSQL service is enabled
      And TNRD Poetry is available
     Then TNRE the python version >= 3.12
      And TNRG the postgresql version >= 17
      And TNRI PostgreSQL service is operational
      And TNRF the nodejs version >= 18
      And TNRH the poetry version >= 1.8

  @dev @ci @prod
  Scenario: TNS Provide Saleor commerce capabilities
     When TNSB build tools are available
      And TNSS Saleor source code is available
      And TNSN Saleor Python virtual environment is available
      And TNSD Saleor Python dependencies are installed
      And TNSP Saleor service definition is present
      And TNSE Saleor service is enabled 
     Then TNSV saleor version >= 3.20
      And TNSO OpenRC manages the running saleor service
      And TNSG Saleor GraphQL endpoint responds successfully
