"""

process_text.py

Fetches, cleans, and chunks text with a TextProcessor class

"""


class TextProcessor: 
    @staticmethod 
    def clean_text(text): 
        cleaned_text = text.strip().replace("\n", "")
        return cleaned_text 
    
    @staticmethod 
    def chunk_text(text, chunk_size):
        words = text.split(" ")
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks 
    
    @staticmethod
    def fetch_text(filename):
        with open(filename, "r") as f:
            content = f.read() 
    
        return content


if __name__ == "__main__":
    # Example Usage 
    text = TextProcessor.fetch_text("data/sample.txt")
    cleaned_text = TextProcessor.clean_text(text) 
    chunks = TextProcessor.chunk_text(cleaned_text, 100) 

    print(*chunks, sep="\n\n") 