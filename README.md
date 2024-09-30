# Recipe Generator

This project is an AI-powered recipe generator that creates unique recipes based on various parameters and ensures diversity in the generated recipes.

## Features

- Generates unique recipes
- Embeds recipes for similarity comparison
- Integrates with a Supabase database for recipe storasge

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the root directory and add the following variables:

```
DEEP_INFRA_API_KEY=your_deep_infra_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Usage

To generate recipes, run the main script:

```bash
python main.py
```

This will start the recipe generation process. The script will continue generating recipes until you stop it manually (Ctrl+C).


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
