import json
import requests
import guidance

# 1. Target Endpoint Initialization (Pre-configured with your GCP VM Public IP)
GCP_VM_IP = "35.238.201.140" 
VENDURE_SHOP_API = f"http://{GCP_VM_IP}:3000/shop-api"

# 2. Structural Guidance Schema Engine Setup
# Forces LLM token selection to cleanly generate strict parameters
@guidance
def enforce_b2b_schema(lm, raw_user_prompt):
    lm += f"Context: Transform raw query to strict commerce schema.\n"
    lm += f"User request: {raw_user_prompt}\n"
    
    # Restrict categorical generation exactly to seed database items
    lm += "Category selection: " + guidance.select(["Electronics", "Appliances", "Furniture"], name="category") + "\n"
    
    # Enforce strict maximum payload constraint via explicit token matching
    lm += "Payload item limit: " + guidance.select(["5", "10", "20"], name="limit") + "\n"
    return lm

# 3. Execute Guidance loop locally against your targeted model instance
# Note: Ensure you have an active model backend configuration set up here.
# By default, we use a small, fast local model or you can swap this with an OpenAI / Gemini API:
# Example for OpenAI: model_backend = guidance.models.OpenAI("gpt-4o")
print("Initializing Guidance model backend...")
model_backend = guidance.models.Transformers("meta-llama/Meta-Llama-3-8B-Instruct")

print("Executing programmatic guidance constraint mapping...")
pipeline_state = model_backend + enforce_b2b_schema("I am looking for a batch of up to ten home computing machines or screens.")

# 4. Extract safe parameter structures from the validation matrix
verified_category = pipeline_state["category"]
verified_limit = int(pipeline_state["limit"])

print(f"Validated parameters extracted: Category = {verified_category}, Limit = {verified_limit}")

# 5. Build a structured GraphQL query payload for Vendure
graphql_payload = {
    "query": """
    query ExecuteConstrainedSearch($options: SearchInput!) {
      search(input: $options) {
        items {
          productId
          productName
          slug
        }
        totalItems
      }
    }
    """,
    "variables": {
        "options": {
            "term": verified_category,
            "skip": 0,
            "take": verified_limit
        }
    }
}

# 6. Fire network request to your cloud infrastructure
http_headers = {"Content-Type": "application/json"}
try:
    print(f"Sending constrained GraphQL query to Vendure at {VENDURE_SHOP_API}...")
    network_response = requests.post(
        url=VENDURE_SHOP_API, 
        json=graphql_payload, 
        headers=http_headers,
        timeout=15
    )
    
    print(f"Server Connection Status: {network_response.status_code}")
    print("Validated Return Payload Structure:")
    print(json.dumps(network_response.json(), indent=2))

except requests.exceptions.RequestException as network_error:
    print(f"\nNetwork processing failed! Error: {network_error}")
    print("Please inspect your GCP firewalls and ensure your VM docker containers are running.")
