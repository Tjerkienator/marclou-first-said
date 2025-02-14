# ADR 001: YouTube Transcript Storage Strategy

## Status
Accepted

## Context
The system needs to store YouTube video transcripts alongside video metadata. We considered two main approaches:
1. Store transcripts in the same MongoDB collection as video documents
2. Store transcripts in a separate MongoDB collection with references to videos

Key considerations included:
- Data access patterns
- Performance implications
- Operational complexity
- Future scalability needs

## Decision
We decided to store transcripts within the video documents in a single MongoDB collection for the following reasons:

### Current Implementation
```python
class Video(BaseModel):
    # ... video metadata fields ...
    transcript: Optional[str]
    transcript_fetched: bool
    transcript_fetched_at: Optional[datetime]
```

### Rationale

#### Advantages of Current Approach
1. **Simplified Data Access**
   - No join operations needed
   - Atomic updates guaranteed
   - Natural data consistency

2. **Current Usage Patterns**
   - Most operations need both video metadata and transcript
   - Primary workflow is sequential: fetch video → get transcript → process words
   - No complex transcript-only queries required

3. **Data Volume Reality**
   - YouTube transcripts typically under 100KB
   - Well within MongoDB's 16MB document limit
   - No multiple transcript versions/languages needed currently

4. **Operational Benefits**
   - Simpler codebase
   - Fewer failure points
   - Easier debugging and maintenance
   - No need for manual referential integrity

#### Considered But Rejected (Separate Collections)
```python
# Potential future structure if needs change
class Transcript(BaseModel):
    video_id: str
    content: str
    language: str = "en"
    version: int = 1
```

This was rejected for now as it would add complexity without providing immediate benefits.

## Consequences

### Positive
- Simpler implementation
- Better data consistency
- Faster development velocity
- Easier maintenance

### Negative
- Less flexible for future transcript variations
- Potentially larger document sizes
- May need migration if requirements change significantly

## Future Triggers for Revisiting
This decision should be revisited if:
1. We need to store multiple transcript versions (e.g., different languages)
2. We implement heavy text analysis requiring transcript-only queries
3. Document sizes become a performance concern
4. We need different access patterns for transcripts vs videos

## Migration Path
If future needs require separate collections, migration path would involve:
1. Creating new transcript collection
2. Moving transcript data to new collection
3. Updating application code to handle separate collections
4. Adding necessary indexes and data integrity checks

## References
- MongoDB document size limits: https://www.mongodb.com/docs/manual/reference/limits/
- YouTube transcript typical sizes and characteristics
- Project requirements and workflow documentation 