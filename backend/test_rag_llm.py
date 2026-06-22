import ollama

question = "How are employee salaries reviewed?"

retrieved_chunk = """
Employee salary policy:

Employees receive annual salary reviews
based on performance evaluations.
"""

prompt = f"""
Answer the question using only the context below.

Context:
{retrieved_chunk}

Question:
{question}

Answer:
"""

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])