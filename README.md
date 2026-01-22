# syntomid-json-export
SynToMid + FL Studio piano roll to unified JSON format. Convert YouTube Synthesia videos and FL piano roll exports into portable, DAW-agnostic note data for generative audio engines.

## Features

- **Screenshot-to-JSON conversion**: Upload piano roll screenshots from FL Studio or other DAWs
- **Web-based interface**: No installation required, browser-based tool
- **CLI tool**: `syntomid_convert.py` for batch processing and automation
- **Unified schema**: Standardized JSON format for note data
- **YouTube Synthesia support**: Extract notes from piano tutorial videos
- **DAW-agnostic**: Works with any piano roll format
- **Generative AI ready**: Structured output for training audio models

## Installation

### Web App (No Installation)
Simply open `screenshot_app.html` in your web browser. No dependencies required.

### CLI Tool

```bash
# Clone the repository
git clone https://github.com/jyee4187/syntomid-json-export.git
cd syntomid-json-export

# Install Python dependencies
pip install -r requirements.txt
```

## Quick Start

### Using the Web App

1. Open `screenshot_app.html` in your browser
2. Drag and drop a piano roll screenshot
3. The app will analyze the image and extract note data
4. Download the resulting JSON file

### Using the CLI

```bash
python syntomid_convert.py input.mid output.json
```

## Usage Examples

### Web App Workflow

1. Screenshot your FL Studio piano roll
2. Upload to the web app
3. Automatic note detection and JSON export
4. Import into your generative model

### CLI Workflow

```bash
# Convert MIDI to JSON
python syntomid_convert.py input_file.mid output_file.json

# Batch convert multiple MIDI files
for f in *.mid; do
  python syntomid_convert.py "$f" "${f%.mid}.json"
done
```

## JSON Schema

Refer to `SCHEMA.md` for detailed documentation of the output format.

## Project Structure

```
syntomid-json-export/
├── README.md              # This file
├── SCHEMA.md              # JSON schema documentation
├── requirements.txt       # Python dependencies
├── syntomid_convert.py    # CLI conversion tool
└── screenshot_app.html    # Web-based screenshot converter
```

## Dependencies

- `mido` - MIDI file processing
- `numpy` - Numerical computations
- `pillow` - Image processing (web app)

## Requirements

- Python 3.8+
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Contributing

Contributions welcome! Please feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open an issue on GitHub.
