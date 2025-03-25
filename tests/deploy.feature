Feature: SC Saleor Commerce Platform on Alpine Linux | BDA

  @dev
  Scenario: SC1 Target a development environment for testing
     When SC1A target environment is configured for development
     Then SC1B the system is configured for development testing

  @ci
  Scenario: SC2 Target a CI environment for verification
     When SC2A target environment is configured for continuous integration
     Then SC2B the system is configured for CI testing

  @prod
  Scenario: SC3 Target a production environment for customers
     When SC3A target environment is configured for production
     Then SC3B the system is configured for production use

  @dev @ci @prod
  Scenario: SC4 Provide a stable Alpine Linux platform
     When SC4A system packages up to date
     Then SC4B OS Alpine Linux 3.21

  @dev @ci @prod
  Scenario: SC5 Enable required runtime environments for Saleor
     When SC5A Python runtime is available
      And SC5B NodeJS runtime is available
      And SC5C SQLite database is available
      And SC5D Poetry is available
     Then SC5E python version >= 3.12
      And SC5F nodejs version >= 18
      And SC5G sqlite version >= 3.48
      And SC5H poetry version >= 1.8

  @dev @ci @prod
  Scenario: SCF Provide Saleor commerce capabilities

     When SCFB build tools are available
     When SCFS Saleor source code is available
     When SCFV Saleor Python virtual environment is available
     When SCFD Saleor Python dependencies are installed
     When SCFO Saleor service definition is present
     When SCFE Saleor service is enabled 
     Then SCFV saleor version >= 3.20
      And SCFO OpenRC manages the running saleor service
      And SCFG Saleor GraphQL endpoint responds successfully
