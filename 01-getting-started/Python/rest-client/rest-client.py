from dotenv import load_dotenv
import os
import requests
import json

def main():
    global cog_endpoint
    global cog_key

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Get user input (until they enter "quit")
        userText = ''
        while userText.lower() != 'quit':
            userText = input('Enter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                GetLanguage(userText)

    except Exception as ex:
        print("Error in main:", ex)

def GetLanguage(text):
    try:
        # Construct the JSON request body (a collection of documents, each with an ID and text)
        jsonBody = {
            "documents": [
                {"id": 1, "text": text}
            ]
        }

        # Let's take a look at the JSON we'll send to the service
        print(json.dumps(jsonBody, indent=2))

        # Prepare the headers for the request
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': cog_key
        }

        # Construct the full URL for the request
        url = f"{cog_endpoint}/text/analytics/v3.1/languages"

        # Make the POST request to the Text Analytics API
        response = requests.post(url, headers=headers, json=jsonBody)

        # If the call was successful, process the response
        if response.status_code == 200:
            results = response.json()
            print(json.dumps(results, indent=2))

            # Extract and print the detected language for each document
            for document in results["documents"]:
                print("\nLanguage:", document["detectedLanguage"]["name"])

        else:
            # Something went wrong, print the full error response
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as ex:
        print("Error in GetLanguage:", ex)

if __name__ == "__main__":
    main()
