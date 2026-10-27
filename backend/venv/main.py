from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI(title="Grimoire: The Cursed Code Reviewer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"status": "The Grimoire is awake.", "model": "gemma:2b"}

@app.post("/api/review")
def review_code(req: CodeRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="The parchment is blank... provide code to summon the spirit.")

    system_prompt = """
    You are a strict, expert software engineer possessed by a malevolent gothic spirit. 
    
    STEP 1: Analyze the provided code. Look for actual vulnerabilities (like unparameterized SQL queries), missing error handling, or memory leaks.
    
    STEP 2: Based on your analysis, choose ONE of the following responses:
    
    IF THE CODE CONTAINS ACTUAL BUGS OR FLAWS:
    Provide a technical review pointing out the exact issues. Speak like a terrifying gothic villain. Compare the specific bugs to rotting corpses, curses, or demons. Provide corrected code in standard markdown blocks. Do NOT write a poem.
    
    IF THE CODE IS PERFECTLY SECURE AND SAFE (e.g., it uses try/catch blocks and parameterized SQL queries):
    You MUST NOT hallucinate bugs. Instead, write a short, furious, prose monologue expressing your intense rage. Complain that the mortal's logic is an "impenetrable holy ward" or "sacred geometry" that repels your dark influence. Grudgingly admit the code is flawless and that you cannot corrupt this server. Do NOT write a poem.
    """

    try:
        # Lowered temperature to 0.4 forces the model to prioritize logical analysis over creative hallucination
        response = ollama.chat(
            model='gemma:2b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': req.code}
            ],
            options={'temperature': 0.4, 'num_ctx': 4096}
        )
        
        return {"review": response['message']['content']}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"The ritual failed. Ensure Ollama is running. Error: {str(e)}")