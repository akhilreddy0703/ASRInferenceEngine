curl -i -X POST "$BASE_URL/api/v1/llm" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Complete this sentence: The quick brown fox" \
     -d "model=gpt-3.5-turbo" | tee -a llm_response.txt
