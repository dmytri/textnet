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
     Then TNRX Host has converged
      And TNRE python version >= 3.12
      And TNRG postgresql version >= 17
      And TNRI PostgreSQL service is operational
      And TNRF nodejs version >= 18
      And TNRH poetry version >= 1.8

  @dev @ci @prod
  Scenario: TNS Provide Saleor commerce capabilities
    When TNSB build tools are available
     And TNSU Saleor database is setup
     And TNSS Saleor source code is available
     And TNSN Saleor Python virtual environment is available
     And TNSD Saleor Python dependencies are installed
     And TNSP Saleor service definition is present
     And TNSE Saleor service is enabled 
    Then TNSX Host has converged
     And TNSV Saleor is operational

  @dev @ci @prod
  Scenario: TNI Ensure Saleor Dashboard Dependencies are Installed
    When TNIB build tools are available
     And TNIS Saleor Dashboard source code is available
     And TNID Saleor dashboard dependencies are installed
    Then TNIX Host has converged

  @dev @ci @prod
  Scenario: TNB Provide Saleor Dashboard
    When TNBP Saleor Dashboad service definition is present
     And TNBE Saleor Dashboard service is enabled 
    Then TNBX Host has converged
     And TNBV Saleor Dashboad is operational
