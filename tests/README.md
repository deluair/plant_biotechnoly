# BIOSIMULATE Tests

This directory contains test scripts for the BIOSIMULATE project, which is a simulation framework for plant biotechnology innovation, regulation, and market dynamics.

## Test Structure

The test suite is organized into several modules, each focusing on different components of the simulation:

- `test_agents.py`: Tests for agent classes (ResearchEntity, CommercialPlayer, RegulatoryBody, MarketParticipant)
- `test_simulation_engine.py`: Tests for the simulation engine and configuration
- `test_economic_market.py`: Tests for economic and market-related components
- `test_technology_regulatory.py`: Tests for technology and regulatory components
- `test_utils.py`: Tests for utility functions and data generators

## Running Tests

### Running All Tests

To run all tests, use the `run_tests.py` script:

```bash
python tests/run_tests.py
```

This will discover and run all test files in the tests directory.

### Running Specific Test Files

To run a specific test file, you can use the unittest module directly:

```bash
python -m unittest tests/test_agents.py
```

### Running Specific Test Cases or Methods

To run a specific test case or method, you can use the unittest module with the following syntax:

```bash
# Run a specific test case
python -m unittest tests.test_agents.TestResearchEntity

# Run a specific test method
python -m unittest tests.test_agents.TestResearchEntity.test_initialization
```

## Test Dependencies

The tests require the following dependencies:

- Python 3.6+
- NumPy
- All dependencies required by the BIOSIMULATE project

## Adding New Tests

When adding new tests, follow these guidelines:

1. Create a new test file named `test_<component>.py` for new components
2. Use the unittest framework and follow the existing test structure
3. Include both unit tests for individual functions and integration tests for component interactions
4. Ensure tests are independent and do not rely on the state from other tests
5. Use appropriate assertions to verify expected behavior

## Test Coverage

The current test suite covers:

- Agent creation and behavior
- Simulation engine initialization and execution
- Economic and market model functionality
- Technology pipeline and innovation processes
- Regulatory framework and approval processes
- Utility functions for data generation

Future improvements to test coverage may include:

- More extensive integration tests
- Performance benchmarks
- Edge case testing
- Stress testing with large agent populations