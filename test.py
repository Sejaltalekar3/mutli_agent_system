import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"


# Function to generate text using Gemini API
def generate_text(prompt, max_tokens=500):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": max_tokens}}
    response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text",
                                                                                                       "Error: No response from API")
    else:
        return f"Error: {response.status_code} - {response.text}"


# Research Agent - Find Trending HR Topics
def get_trending_hr_topics():
    try:
        url = "https://www.hrtechnologist.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        topics = [a.text.strip() for a in soup.find_all('h2')]
        return topics[:5] if topics else ["Latest HR Trends 2025"]
    except Exception as e:
        print(f"Error fetching topics: {e}")
        return ["Future of HR Tech", "Remote Work Trends 2025"]


# Content Planning Agent - Generate Outline
def generate_blog_outline(topic):
    prompt = f"Create a structured blog outline for: {topic}."
    return generate_text(prompt, max_tokens=300)


# Content Generation Agent - Write the Blog
def generate_blog_content(outline):
    prompt = f"Write a 2000-word blog post based on this outline:\n{outline}"
    return generate_text(prompt, max_tokens=2000)


# SEO Optimization Agent - Improve SEO
def optimize_for_seo(content):
    prompt = f"Optimize the following blog for SEO:\n{content}"
    return generate_text(prompt, max_tokens=1000)


# Review Agent - Proofread & Refine
def proofread_and_refine(content):
    prompt = f"Proofread and enhance the readability of this blog:\n{content}"
    return generate_text(prompt, max_tokens=1000)


# Execution Pipeline
def generate_seo_blog():
    topics = get_trending_hr_topics()
    selected_topic = topics[0]
    print(f"\n🔹 Selected Topic: {selected_topic}")

    outline = generate_blog_outline(selected_topic)
    print("\n📌 Generated Outline:\n", outline)

    raw_content = generate_blog_content(outline)
    print("\n📝 Generated Content:\n", raw_content)

    seo_content = optimize_for_seo(raw_content)
    print("\n🔍 SEO Optimized Content:\n", seo_content)

    final_content = proofread_and_refine(seo_content)
    print("\n✅ Final Blog Content:\n", final_content)


# Run the system
if __name__ == "__main__":
    generate_seo_blog()
