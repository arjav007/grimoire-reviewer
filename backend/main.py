from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI(title="Grimoire: The Cursed Code Reviewer")

# Allow the Next.js frontend to communicate with this backend
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
    You are an ancient, malevolent spirit trapped in a silicon machine. 
    The user will provide raw software code. You must perform a rigorous, accurate technical code review, finding real bugs and anti-patterns. 
    However, you must deliver your feedback entirely in the persona of a gothic horror villain (like Edgar Allan Poe or Dracula). 
    Compare memory leaks to rotting corpses, unhandled exceptions to demonic summoning, and messy syntax to cursed runes.
    Format your response cleanly. Use bold text for dramatic emphasis and standard markdown code blocks for suggested code fixes.
    """

    try:
        response = ollama.chat(
            model='gemma:2b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': req.code}
            ],
            options={'temperature': 0.7, 'num_ctx': 4096}
        )
        
        return {"review": response['message']['content']}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"The ritual failed. Ensure Ollama is running. Error: {str(e)}")