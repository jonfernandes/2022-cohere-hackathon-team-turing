# Traditional Customer Service Web Chat is Dead: Here's why Cohere's LLM matters.
## Instructions
### Prerequisites
- See requirements.txt file
### Installation
1. install prerequisites
2. Navigate to project folder in your terminal and execute `pipenv install`

### Running
 1. No dotenv has been setup for this project so please add your Co:here API key to `./ChatApp/main.py` (line 25)
 2. `pipenv shell` -> to enter configured python environment 
 3. `cohere_demo/bin/uvicorn ChatApp.main:app --reload` -> to run the application (cohere_demo is the virtual environment)
 4. navigate to `127.0.0.1:8000/customer-chat` for the customer view and `127.0.0.1:8000/customer-support` for the customer support view
 
## Example prompts as customer
 - Hey can you help me with my cold frame I purchased from you guys?
 - What is the height at the back in cm for the Halls Standard Cold Frame?
 - What is the height at the back in cm for the Halls Standard Cold Frame with Toughened Glass?
 - My Halls Standard Cold Frame size is off, what are the measurements supposed to be?