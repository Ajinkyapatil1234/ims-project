## Approach

This project was designed using a simple and scalable architecture:

- Used FastAPI for backend APIs
- Used PostgreSQL as the source of truth
- Used Redis as a queue for async processing
- Implemented a worker to process signals
- Added debounce logic using Redis TTL
- Focused on reliability and simplicity over complexity

The system ensures that signal ingestion is decoupled from processing, helping handle burst traffic.
