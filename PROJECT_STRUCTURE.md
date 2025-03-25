# Project Structure

This document outlines the purpose and organization of the files and directories in this repository.

## Top-Level Directories

### `.`: Root directory

Contains files related to the Behaviour-Driven Automation (BDA) setup.
These are used for development, testing, and CI/CD, but are not part of the
final deployed system.

### `target` directory

Contains files related to the deploy target host for dev and tests enviroments.
This is where the system will be depoloyed to by the BDA steps in dev and test
enviroments.

### `tests` directory

Contains the BDA and ATDD steps that provide the self-describing, and
self-verifying automation steps (BDA) as well as the executable acceptance
criteria (ATDD)

## Key Files

### `.`: Root directory

* `Dockerfile`: Dockerfile for running BDA/ATDD Steps in Apply job
* `manifest.yaml`: Kubernetes manifest for the Apply, uses the above Dockerfile
* `Tiltfile`: Configuration file for Tilt, used to automate the deployment the Target host and run the Apply job

### Target Directory (`target`):

* `Dockerfile`: Dockerfile for target host to be used in Dev and Test enviroments
* `manifest.yaml`: Kubernetes manifest for deploying the target host.

## Relationship between BDA and Target System

The BDA setup in the root directory is used to:

1.  Provision a test host as described in the `target` directory, using Tilt
2.  Deploy the system to the target host.
3.  Run automated tests (defined in the `tests` directory) to verify the correct deployment and configuration of the target system.

