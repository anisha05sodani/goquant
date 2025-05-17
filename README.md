# GoQuant Trading Simulator

A high-performance trade simulator that leverages real-time market data to estimate transaction costs and market impact.

## Features

- Real-time L2 orderbook data processing
- Market impact modeling using Almgren-Chriss model
- Slippage estimation using regression modeling
- Maker/Taker proportion prediction
- Interactive UI for parameter input and result visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/goquant.git
cd goquant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. For development, install additional dependencies:
```bash
pip install -r requirements-dev.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Development

### Running Tests
```bash
make test
```

### Code Formatting
```bash
make format
```

### Linting
```bash
make lint
```

### Documentation
```bash
make docs
```

## Project Structure

- `src/`: Source code
  - `core/`: Core functionality
  - `models/`: Trading models
  - `ui/`: User interface
  - `config/`: Configuration
- `tests/`: Test files
- `docs/`: Documentation
- `logs/`: Log files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 