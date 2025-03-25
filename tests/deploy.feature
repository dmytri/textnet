Feature: TN TextNet Saleor Commerce Based Platform on Alpine Linux | BDA

  @dev
  Scenario: TND Target a development environment for testing
     When TNDA the target environment is configured for development
     Then TNDB the system is configured for development testing

  @ci
  Scenario: TNC Target a CI environment for verification
     When TNCA the target environment is configured for continuous integration
     Then TNCB the system is configured for CI testing

  @prod
  Scenario: TNP Target a production environment for customers
     When TNPA the target environment is configured for production
     Then TNPB the system is configured for production use

  @dev @ci @prod
  Scenario: TNA Provide a stable Alpine Linux platform
     When TNAA the system packages up to date
     Then TNAB OS Alpine Linux 3.21

  @dev @ci @prod
  Scenario: TNR Enable required runtime environments for Saleor
     When TNRA Python runtime is available
      And TNRB NodeJS runtime is available
      And TNRC SQLite database is available
      And TNRD Poetry is available
     Then TNRE the python version >= 3.12
      And TNRF the nodejs version >= 18
      And TNRG the sqlite version >= 3.48
      And TNRH the poetry version >= 1.8

  @dev @ci @prod
  Scenario: TNS Provide Saleor commerce capabilities
     When TNSB build tools are available
      And TNSS Saleor source code is available
      And TNSV Saleor Python virtual environment is available
      And TNSD Saleor Python dependencies are installed
      And TNSO Saleor service definition is present
      And TNSE Saleor service is enabled 
     Then TNSV saleor version >= 3.20
      And TNSO OpenRC manages the running saleor service
      And TNSG Saleor GraphQL endpoint responds successfully
