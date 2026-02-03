from datetime import datetime
import random
from ddgs import DDGS
from .schemas import *

def get_current_time() -> str:
    return  datetime.now().strftime(format=r'%Y-%m-%d %H:%M:%S')

def get_dad_joke() -> str:
    dad_jokes = [
        "I’m reading a book on anti-gravity—it’s impossible to put down.",
        "I told my computer I needed a break, and it said: no problem, I’ll go to sleep.",
        "Why don’t eggs tell jokes? They’d crack each other up.",
        "I used to play piano by ear, but now I use my hands.",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "I asked my dog what’s two minus two—he said nothing.",
        "I don’t trust stairs. They’re always up to something.",
        "Why did the math book look sad? Because it had too many problems.",
        "I used to hate facial hair, but then it grew on me.",
        "What do you call fake spaghetti? An impasta."
    ]
    return random.choice(dad_jokes)

def web_search(query: str) -> dict:
    num_results=3
    results=[]
    with DDGS() as ddgs:
        for ans in ddgs.text(query, safesearch='off'):
            if len(results)>num_results: break
            results.append({
                'title': ans.get('title','').strip(),
                'snippet': ans.get('body', '').strip(),
                'url': ans.get('href','').strip()
            })
    return {
        'query': query,
        'results': results
    }

def write_email(response: EmailResponse) -> EmailResponse:
    return response

def write_essay(response: EssayResponse) -> EssayResponse:
    return response

def general_response(response: GeneralResponse) -> GeneralResponse:
    return response

if __name__=='__main__':
    query='What happened to vecna in stranger things season 5?'
    result = web_search(query=query)
    for x in range(3):
        print(f"\n\n{result['results'][x]['snippet']}")