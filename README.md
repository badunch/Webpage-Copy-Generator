# Webpage Copy Generator

This script generates detailed and engaging copy for multiple webpages based on user-provided page names. The content is generated using Google's generative AI models.

## Features

- Prompt user for the names of the webpages.
- Generate copy for each webpage.
- Save the generated copy in a structured format in a dedicated directory.
- Handles rate limits and retries API calls in case of errors.

## Requirements

- Python 3.7 or higher
- `google-api-core`
- `google-generativeai`
- `python-dotenv`

## Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/your-username/webpage-copy-generator.git
   cd webpage-copy-generator
   ```

2. **Create a Virtual Environment and Install Dependencies**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project and add your Google API key:

   ```sh
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. **Run the Script**

   ```sh
   python generate_copy.py
   ```

2. **Follow the Prompts**

   - You will be prompted to select a model from the available list.
   - Enter the names of the webpages you need copy for, separated by commas.

3. **Generated Copy**

   The generated copy for each webpage will be saved in a directory named `web_copy_<timestamp>`, where `<timestamp>` is the date and time when the script was run.

## Available Models

The script supports the following models:

1. **gemini-1.5-flash-latest**
   - Powerful model capable of handling text and image inputs, optimized for various language tasks like code generation, text editing, and problem-solving.
   - Rate Limit: 2 queries per minute
   - Daily Limit: 1000 queries

2. **gemini-1.0-pro-latest**
   - Versatile model for text generation and multi-turn conversations, suitable for zero-shot, one-shot, and few-shot tasks.
   - Rate Limit: 60 queries per minute

3. **gemini-1.5-pro-latest**
   - Versatile model for text generation and multi-turn conversations, suitable for zero-shot, one-shot, and few-shot tasks.
   - Rate Limit: 60 queries per minute

## Error Handling

The script includes retry logic to handle API call errors such as invalid input, deadline exceeded, and quota limit reached.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
```

### Instructions:

1. Replace `your-username` in the clone URL with your actual GitHub username.
2. Ensure that you create a `requirements.txt` file with the necessary dependencies.
3. Add the actual MIT License text in a `LICENSE` file if it's not already included.
