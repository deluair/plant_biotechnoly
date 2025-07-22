# BIOSIMULATE

## Comprehensive Plant Biotechnology Industry Ecosystem Simulation

This project implements a sophisticated multi-agent simulation modeling the global plant biotechnology industry ecosystem from 2025-2035, incorporating realistic market dynamics, regulatory frameworks, technological advancement pathways, and stakeholder interactions across different geographical regions and market segments.

## Project Structure

```
biosimulate/
├── agents/                  # Agent-based modeling components
│   ├── agent_factory.py    # Agent creation and initialization
│   ├── base_agent.py       # Base agent class
│   ├── commercial_player.py # Commercial entities and market participants
│   ├── market_participant.py # Market interaction behaviors
│   ├── regulatory_body.py  # Regulatory agencies and oversight
│   └── research_entity.py  # Research institutions and R&D
├── economic/                # Economic modeling frameworks
│   └── market.py           # Market dynamics and product registration
├── regulatory/              # Regulatory framework simulation
│   ├── approval.py         # Product approval processes
│   └── framework.py        # Regulatory oversight and compliance
├── simulation/              # Core simulation mechanics
│   ├── config.py           # Configuration management
│   ├── engine.py           # Main simulation engine
│   ├── events.py           # Event handling and scheduling
│   └── metrics.py          # Performance metrics and analytics
├── technology/              # Technology innovation pipeline models
│   ├── innovation.py       # Innovation processes and R&D
│   └── pipeline.py         # Technology development pipelines
├── utils/                   # Utility functions and helpers
│   ├── data_generator.py   # Synthetic data generation
│   ├── file_utils.py       # File I/O operations
│   ├── logging_config.py   # Logging configuration
│   └── validation.py       # Data validation utilities
└── visualization/           # Data visualization and dashboards
    ├── geo_visualization.py # Geographic visualizations
    ├── interactive.py       # Interactive dashboards
    ├── network_visualization.py # Network analysis plots
    └── plots.py            # Statistical plots and charts
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd plant_biotechnoly
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Simulation

```bash
# Run with default baseline scenario
python -m biosimulate.run_simulation

# Run with verbose output
python -m biosimulate.run_simulation --verbose

# Run with custom scenario
python -m biosimulate.run_simulation --scenario custom_scenario
```

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test modules
python -m pytest tests/test_agents.py
python -m pytest tests/test_simulation_engine.py
```

## Features

### Core Simulation Components
- **Multi-Agent System**: 670+ agents including commercial players, research entities, and regulatory bodies
- **Market Dynamics**: Product registration, pricing models, and competitive interactions
- **Regulatory Framework**: Approval processes, compliance monitoring, and policy impacts
- **Technology Pipeline**: Innovation cycles, R&D investments, and technology transfer
- **Economic Modeling**: Market valuation, investment flows, and financial metrics

### Simulation Capabilities
- **Temporal Modeling**: 11-year simulation period (2025-2035) with annual progression
- **Scenario Analysis**: Baseline and custom scenario configurations
- **Geographic Scope**: Multi-regional regulatory and market frameworks
- **Stochastic Events**: Random events affecting market and regulatory conditions
- **Performance Metrics**: Comprehensive tracking of industry KPIs

### Output and Analytics
- **CSV Export**: Detailed simulation results with timestamped outputs
- **Logging**: Comprehensive logging with configurable verbosity levels
- **Visualization**: Built-in plotting and dashboard capabilities
- **Metrics Tracking**: Agent performance, market dynamics, and regulatory outcomes

## Recent Updates

- ✅ Fixed agent factory initialization issues
- ✅ Resolved technology pipeline method naming conflicts
- ✅ Added missing regulatory framework methods
- ✅ Corrected market product registration logic
- ✅ Implemented comprehensive error handling and logging
- ✅ Successfully validated simulation execution with 547 data points generated

## Output Files

Simulation results are saved to the `results/` directory with timestamped filenames:
- `baseline_YYYYMMDD_HHMMSS.csv` - Main simulation output data
- Logs are saved to `logs/` directory for debugging and analysis

## Configuration

The simulation uses configuration files in `biosimulate/simulation/config.py` to define:
- Agent populations and distributions
- Market parameters and dynamics
- Regulatory framework settings
- Technology development parameters
- Economic modeling assumptions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure functionality
5. Submit a pull request

## License

MIT