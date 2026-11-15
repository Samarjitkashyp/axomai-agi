import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from axomai.db.models import DocumentChunk, Document
from axomai.db.session import SyncSessionLocal

class DocumentRetriever:
    """
    Retrieves the most relevant chunks from PostgreSQL for a given document and query.
    Extracts targeted evidence with exact page numbers to feed into Z1 Alpha's reasoning brain.
    """
    def __init__(self, top_k: int = 4):
        self.top_k = top_k

    def retrieve(
        self,
        document_id: str,
        query: str,
        target_page: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top relevant chunks from PostgreSQL for the document.
        """
        with SyncSessionLocal() as db:
            chunks_query = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id)
            
            # If a specific page was requested, prioritize that page's chunks
            if target_page is not None:
                page_chunks = chunks_query.filter(DocumentChunk.page_number == target_page).all()
                if page_chunks:
                    return [self._format_chunk(c, score=1.0) for c in page_chunks]

            all_chunks = chunks_query.all()
            if not all_chunks:
                return []

            # Scoring based on keyword token overlap and term frequency
            query_tokens = set(re.findall(r'\w+', query.lower()))
            # Remove very common stop words
            stop_words = {"the", "is", "at", "which", "on", "and", "a", "an", "in", "to", "for", "with", "par", "kya", "hai", "me", "ko", "se"}
            filtered_tokens = {w for w in query_tokens if len(w) > 2 and w not in stop_words}

            scored_chunks = []
            for chunk in all_chunks:
                text_lower = chunk.content.lower()
                chunk_tokens = set(re.findall(r'\w+', text_lower))
                
                # Match score
                overlap = len(filtered_tokens.intersection(chunk_tokens))
                # Boost if table
                if chunk.content_type == "table":
                    overlap += 0.5

                if overlap > 0:
                    scored_chunks.append((overlap, chunk))

            # Sort descending by score
            scored_chunks.sort(key=lambda x: x[0], reverse=True)

            # Return top_k
            results = []
            if scored_chunks:
                for score, chunk in scored_chunks[:self.top_k]:
                    results.append(self._format_chunk(chunk, score=float(score)))
            else:
                # Fallback to first 2-3 chunks if no explicit keyword matched
                for chunk in all_chunks[:self.top_k]:
                    results.append(self._format_chunk(chunk, score=0.1))

            return results

    def _format_chunk(self, chunk: DocumentChunk, score: float) -> Dict[str, Any]:
        return {
            "chunk_id": chunk.id,
            "page_number": chunk.page_number,
            "content_type": chunk.content_type,
            "content": chunk.content,
            "metadata": chunk.chunk_metadata,
            "score": score
        }

retriever = DocumentRetriever()

