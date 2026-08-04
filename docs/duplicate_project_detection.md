# AI-Based Duplicate Project Detection Documentation (#608)

DevLink provides an **AI-Powered & Hybrid Duplicate Project Detection System** to compare newly submitted or drafted projects against existing projects across the platform, preventing duplicate submissions while allowing developers a manual override when appropriate.

---

## 1. Hybrid Similarity Scoring Architecture

The duplicate detection engine combines four complementary similarity techniques to ensure high precision and sub-millisecond performance:

1. **AI Semantic Embedding Similarity**:
   - Uses OpenAI (`text-embedding-3-small`) embeddings to compute high-dimensional cosine similarity vectors.
2. **Title Edit Distance & Token Overlap**:
   - Combines normalized Levenshtein edit distance and Jaccard token overlap for project titles.
   - High title match (> 85%) automatically boosts duplicate confidence.
3. **Description Content Overlap**:
   - Token intersection and coverage containment over project summaries and long descriptions.
4. **Tech Stack & Tag Match**:
   - Compares shared programming languages, frameworks, and skill tags.

---

## 2. Duplicate Detection API Reference

### Check Duplicate Endpoint
`POST /api/v1/projects/check-duplicate` (and `/api/projects/check-duplicate`)

**Request Payload:**
```json
{
  "title": "Realtime Collaboration Workspace",
  "description": "A collaborative developer workspace with real-time text editing and audio chat.",
  "tags": ["react", "fastapi", "websockets"],
  "similarity_threshold": 0.65,
  "limit": 5
}
```

**Response Payload:**
```json
{
  "has_duplicates": true,
  "max_similarity_score": 0.885,
  "threshold_used": 0.65,
  "manual_override_allowed": true,
  "suggested_projects": [
    {
      "project_id": "b1a2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Realtime Developer Workspace",
      "slug": "realtime-developer-workspace",
      "description": "Collaborative developer workspace with real-time code sharing...",
      "similarity_score": 0.885,
      "confidence_score": 88.5,
      "is_duplicate": true,
      "match_reasons": [
        "Nearly identical project title (91% title match)",
        "High description similarity",
        "Matching tech stack/tags: react, websockets"
      ]
    }
  ]
}
```

---

## 3. Project Creation Guard & Manual Override Flow

When a user submits a new project via `POST /api/v1/projects`:

1. By default, `allow_duplicate` is `false`.
2. The platform performs an automatic similarity check against existing projects.
3. If a potential duplicate is detected (similarity score >= `0.80`):
   - The server responds with `HTTP 409 Conflict` containing the list of matching projects, confidence scores, and reasons.
4. **Manual Override**:
   - If the user confirms that their project is distinct or wants to proceed anyway, they resubmit with `"allow_duplicate": true` in the request body, bypassing the duplicate block.

---

## 4. Running Tests

Run backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_duplicate_project_detection.py -v
```

Expected result: **6 passed**.
