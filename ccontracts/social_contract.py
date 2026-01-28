# { "Depends": "py-genlayer:test" }
from genlayer import *

class WebScraper(gl.Contract):
    result: str
    
    def __init__(self):
        self.result = ""
    
    @gl.public.write
    def scrape(self, url: str) -> str:
        def fetch():
            content = gl.get_webpage(url, mode='text')
            return content[:500]
        
        self.result = gl.eq_principle_strict_eq(fetch)
        return self.result
    
    @gl.public.write
    def check_word(self, url: str, word: str) -> str:
        def check():
            content = gl.get_webpage(url, mode='text')
            if word.lower() in content.lower():
                return f"Found '{word}'!"
            return f"'{word}' not found"
        
        return gl.eq_principle_strict_eq(check)
