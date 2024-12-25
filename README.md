# Recipe Generator

This project is an AI-powered recipe generator that creates unique recipes based on provided list of recipe names.

## Features

- Generates unique recipes using llama
- Embeds recipes for similarity comparison

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   Create a `.env.local` file in the root directory and add the necessary environment variables (refer to `.env.example`).

## Usage

To generate recipes, run the main script:

```bash
python main.py
```

This will start the recipe generation process using by reading all recipe names in recipes.md and generating complete recipes using llama. The script will continue generating recipes until you stop it manually (Ctrl+C).

After the generation of each recipe, the ingestion micro service is called to save and index the recipe, so you must have the recipe ingestion service already running before running the recipe generator.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
