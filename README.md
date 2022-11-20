# co:here chat
## Installation
1. See requirements.txt file

## Running
 1. The API key is stored in `COHERE_API_KEY.json`. The file has this format:
    - {
    "API_KEY": "xxxxxxxx"
    }
 2. A virtual environment cohere_demo was created for this project. 
 3. Use `cohere_demo/bin/uvicorn ChatApp.main:app --reload` to run the application.
 4. In your browser, go to:
    - `127.0.0.1:8000/customer-chat` for the customer view and 
    - `127.0.0.1:8000/customer-support` for the customer support view
 5. Enter a conversation between a customer and customer support. 
 6. When either the customer or customer support leaves the conversation, a pdf file is automatically created in `ChatApp/call_logs`.
    This contains:
    - The date and time that the chat took place.
    - The customer support worker ID: This is fixed for now but can be whichever user signed into the system.
    - The customer ID. This is fixed for now but can integrate with business systems to get customer ID based on Order ID for example.
    - The duration of the chat
    - The chat sentiment [positive|negative|neutral] with associated confidence score. (This is determined using sentiment analysis and co:here Classify) 
    - The chat summary (This is created using co:here Generate)
    - A full log of the chat for auditing purposes.