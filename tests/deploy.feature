Feature: BDA | Deployment on Alpine Linux

  @dev
  Scenario: Target environment is set to dev
     When set target environment to dev

  @ci
  Scenario: Target environment is set to ci
     When set target environment to ci

  @prod
  Scenario: Target environment is set to prod
     When set target environment to prod

  @dev @ci @prod
  Scenario: Ensure Alpine Linux 3.21 with required packages
     When system packages up to date
     Then OS Alpine Linux 3.21

  @dev @ci @prod
  Scenario: Ensure Saleor Dependencies Are Installed
     When python installed
      And nodejs installed
      And sqlite installed
     Then python version >= 3.12
      And nodejs version >= 18
      And sqlite version >= 3.48.0

  @dev @ci @prod
  Scenario: Install Saleor Core
     Given Saleor dependencies are installed
     When install saleor core
     Then saleor version >= 3.14
      And saleor service is running
