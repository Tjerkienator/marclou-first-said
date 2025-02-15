# Process Unique Words

Story: As a system, I need to extract unique words from a video's transcript and check if they have been tweeted before to maintain originality.

Acceptance Criteria:

- Retrieve transcripts from MongoDB that have not yet been processed, sorted by the published_at date in ascending order. 
- Tokenize transcripts into individual words, removing duplicates.
- Normalize words (convert to lowercase, remove punctuation, and handle contractions).
- Check MongoDB if each word has already been stored.
- Insert new words into the MongoDB words collection with a tweeted: false flag and a timestamp.
- Store metadata such as the originating video ID for each word.
- the focuss lies on writing modular code.
- ensure any new packages are installed using python poetry.
- manage the init files for functions and services imports.
- manage the env variables through the dependencies.py file.