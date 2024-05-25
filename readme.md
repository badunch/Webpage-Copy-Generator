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
