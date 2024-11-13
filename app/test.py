import requests
import json
import httpx
# Define the endpoint URL

# Define the list of questions
questions = [
    "What is the scientific name of cows?",
    "When did the domestication of cows begin?",
    "What were the ancestors of modern cows called?",
    "What are the early uses of cows by humans?",
    "How did domesticated cows spread to different parts of the world?",
    "What role did cows play in ancient Egypt?",
    "What type of diet do cows have?",
    "How many chambers does a cow's stomach have?",
    "What are the names of the chambers in a cow's stomach?",
    "How does the microbial community in the rumen aid in digestion?",
    "What is the gestation period of cows?",
    "How often do cows typically give birth?",
    "What factors influence the reproductive cycle of cows?",
    "How do cows communicate within their social structures?",
    "What are some common dairy breeds of cows?",
    "What breed is known for producing high butterfat content milk?",
    "What are some characteristics of Holstein cows?",
    "What is unique about Guernsey milk?",
    "What are some common beef breeds of cows?",
    "What makes Wagyu beef famous?"
]

# Define the payload template


# Initialize an empty dictionary to store the results
async def dataset_generator(questions,chatbot_id, token, model_id):
    endpoint_url = "http://127.0.0.1:8000/api/chatbot/chat_aws"

    payload_template = {
        "chatbot_id": chatbot_id,
        "token": token,
        "model_id": model_id
    }
    results = {}
    async with httpx.AsyncClient() as client:
        for idx, question in enumerate(questions, start=1):
            print(f"{idx}: {question}")
            # Prepare the payload with the current question
            payload = payload_template.copy()
            payload["question"] = question
            
            try:
                # Send the POST request to the endpoint
                response = await client.post(endpoint_url, json=payload)
                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the response JSON
                    response_data = response.json()
                    # Store the result in the dictionary
                    results[idx] = {
                        "question": question,
                        "answer": response_data.get("answer", ""),
                        "ground_truth": response_data.get("answer", ""),
                        "contexts": response_data.get("context", "")
                    }
                else:
                    # Handle the case where the request failed
                    results[idx] = {
                        "question": question,
                        "answer": "Request failed with status code {}".format(response.status_code),
                        "ground_truth": "",
                        "contexts": [""]
                    }
            except Exception as e:
                # Handle any exceptions that occur during the request
                results[idx] = {
                    "question": question,
                    "answer": "An error occurred: {}".format(str(e)),
                    "ground_truth": "",
                    "contexts": [""]
                }

    return results
    # Save the results to a JSON file
    # with open(f'{file_loaction}/results.json', 'w') as f:
    #     json.dump(results, f, indent=4)







if __name__ == "__main__":
    payload = {
        "chatbot_id": "37",
        "token": "gg",
        "model_id": "1",
        "question":"what is cow"
    }
    # response = requests.post(endpoint_url, json=payload)
    # print(response.json())
    print(dataset_generator(questions,"37","gg","1"))