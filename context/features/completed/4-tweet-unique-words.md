# Tweet Unique Words

Story: As a system, I need to post each unique word from the database to Twitter and mark it as tweeted to ensure words are not repeated.

Acceptance Criteria:

- Retrieve the next untweeted word from MongoDB.
- the word should be the "oldest" untweeted word.
- Authenticate and connect to Twitter API using Tweepy.
- Post the word as a standalone tweet.
- Update the MongoDB record to set tweeted: true.
- Handle rate limits and API errors with appropriate retry mechanisms.
- Log all tweet activity for debugging and analysis.
- the focuss lies on writing modular code.
- ensure any new packages are installed using python poetry.
- manage the init files for functions and services imports.
- manage the env variables through the dependencies.py file.
- each time the function is called it should only tweet 1 single time.

Additional Notes:
- data base handler is in the database.py file.
- create new needed env variables in .env.example file.