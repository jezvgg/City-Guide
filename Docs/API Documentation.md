# API Documentation for CLIP Service

## GET /get_by_prompt/«city»

### Parameters
- **city** (required): City code to specify the index to use. Available options: 'nino', 'yaros', 'vlad', 'ekb'.

### Request
- **Method**: GET
- **Endpoint**: /get_by_prompt/«city»
- **Body**: 
{
    "prompt": "<your_prompt_text>"
}

### Response
- **Body**: Indexes related to the prompt text.

## POST /get_by_image/«city»

### Parameters
- **city** (required): City code to specify the index to use. Available options: 'nino', 'yaros', 'vlad', 'ekb'.
  
### Request
- **Method**: POST
- **Endpoint**: /get_by_image/«city»
- **Body**: Image file for processing.

### Response
- **Body**: Indexes related to the image content.
