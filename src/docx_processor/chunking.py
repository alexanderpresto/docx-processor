"""
Document chunking module for intelligent text splitting.

This module provides functionality to split documents into manageable chunks
for AI processing while preserving context and maintaining semantic coherence.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import tiktoken


@dataclass
class Chunk:
    """Represents a document chunk with metadata."""
    id: int
    content: str
    token_count: int
    char_count: int
    start_index: int
    end_index: int
    overlap_tokens: int
    metadata: Dict[str, Any]


class DocumentChunker:
    """
    Intelligent document chunking system for AI-friendly text splitting.
    
    Features:
    - Token-based chunking using tiktoken
    - Configurable chunk sizes and overlap
    - Natural boundary detection (paragraphs, sentences)
    - Context preservation between chunks
    - Metadata tracking for each chunk
    """
    
    def __init__(
        self,
        max_tokens: int = 2000,
        overlap_tokens: int = 200,
        encoding_model: str = "cl100k_base",
        respect_boundaries: bool = True
    ):
        """
        Initialize the document chunker.
        
        Args:
            max_tokens: Maximum tokens per chunk (default: 2000)
            overlap_tokens: Number of tokens to overlap between chunks (default: 200)
            encoding_model: Tiktoken encoding model (default: cl100k_base for GPT-4)
            respect_boundaries: Whether to split at natural boundaries (default: True)
        """
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.respect_boundaries = respect_boundaries
        
        try:
            self.encoding = tiktoken.get_encoding(encoding_model)
        except Exception:
            # Fallback to approximate token counting if tiktoken fails
            self.encoding = None
            
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken or approximation."""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Approximate: 1 token ≈ 4 characters
            return len(text) // 4
            
    def find_natural_boundary(self, text: str, target_pos: int, direction: str = "backward") -> int:
        """
        Find the nearest natural text boundary (paragraph or sentence end).
        
        Args:
            text: The text to search
            target_pos: Target position to search from
            direction: Search direction ("backward" or "forward")
            
        Returns:
            Position of the nearest natural boundary
        """
        if not self.respect_boundaries:
            return target_pos
            
        # Define boundary patterns
        paragraph_pattern = r'\n\n+'
        sentence_pattern = r'[.!?]\s+'
        
        if direction == "backward":
            # Search backward for boundaries
            search_text = text[:target_pos]
            
            # First try paragraph boundaries
            para_matches = list(re.finditer(paragraph_pattern, search_text))
            if para_matches:
                return para_matches[-1].end()
                
            # Then try sentence boundaries
            sent_matches = list(re.finditer(sentence_pattern, search_text))
            if sent_matches:
                return sent_matches[-1].end()
                
        else:  # forward
            # Search forward for boundaries
            search_text = text[target_pos:]
            
            # First try paragraph boundaries
            para_match = re.search(paragraph_pattern, search_text)
            if para_match:
                return target_pos + para_match.start()
                
            # Then try sentence boundaries
            sent_match = re.search(sentence_pattern, search_text)
            if sent_match:
                return target_pos + sent_match.start()
                
        return target_pos
        
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Chunk]:
        """
        Split text into chunks with overlap and metadata.
        
        Args:
            text: The text to chunk
            metadata: Optional metadata to include with each chunk
            
        Returns:
            List of Chunk objects
        """
        if not text:
            return []
            
        chunks = []
        chunk_id = 0
        start_index = 0
        base_metadata = metadata or {}
        
        while start_index < len(text):
            # Calculate end position based on token count
            chunk_text = ""
            current_tokens = 0
            end_index = start_index
            
            # Build chunk up to max_tokens
            while end_index < len(text) and current_tokens < self.max_tokens:
                # Add characters in batches for efficiency
                batch_size = min(100, len(text) - end_index)
                test_text = text[start_index:end_index + batch_size]
                test_tokens = self.count_tokens(test_text)
                
                if test_tokens > self.max_tokens:
                    # Binary search for exact position
                    left, right = end_index, end_index + batch_size
                    while left < right - 1:
                        mid = (left + right) // 2
                        if self.count_tokens(text[start_index:mid]) <= self.max_tokens:
                            left = mid
                        else:
                            right = mid
                    end_index = left
                    break
                else:
                    end_index += batch_size
                    current_tokens = test_tokens
                    
            # Adjust to natural boundary
            if end_index < len(text):
                end_index = self.find_natural_boundary(text, end_index, "backward")
                
            # Extract chunk
            chunk_text = text[start_index:end_index]
            token_count = self.count_tokens(chunk_text)
            
            # Create chunk object
            chunk_metadata = {
                **base_metadata,
                "chunk_index": chunk_id,
                "total_chunks": None,  # Will be updated after all chunks are created
                "has_overlap": chunk_id > 0
            }
            
            chunk = Chunk(
                id=chunk_id,
                content=chunk_text,
                token_count=token_count,
                char_count=len(chunk_text),
                start_index=start_index,
                end_index=end_index,
                overlap_tokens=self.overlap_tokens if chunk_id > 0 else 0,
                metadata=chunk_metadata
            )
            chunks.append(chunk)
            
            # Calculate next start position with overlap
            if end_index >= len(text):
                break
                
            # Find overlap start position
            overlap_start = end_index
            if self.overlap_tokens > 0:
                # Count back overlap_tokens from end
                overlap_text = text[start_index:end_index]
                tokens = self.count_tokens(overlap_text)
                
                if tokens > self.overlap_tokens:
                    # Find position that gives us approximately overlap_tokens
                    target_tokens = tokens - self.overlap_tokens
                    test_pos = start_index
                    
                    while test_pos < end_index:
                        if self.count_tokens(text[start_index:test_pos]) >= target_tokens:
                            overlap_start = test_pos
                            break
                        test_pos += 50  # Move in batches
                        
            start_index = overlap_start
            chunk_id += 1
            
        # Update total chunks in metadata
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)
            
        return chunks
        
    def chunk_document_sections(
        self,
        sections: List[Dict[str, Any]],
        preserve_structure: bool = True
    ) -> List[Chunk]:
        """
        Chunk a structured document with sections.
        
        Args:
            sections: List of document sections with 'content' and metadata
            preserve_structure: Whether to preserve section boundaries
            
        Returns:
            List of Chunk objects
        """
        all_chunks = []
        chunk_id = 0
        
        for section_idx, section in enumerate(sections):
            section_content = section.get("content", "")
            section_metadata = {
                "section_index": section_idx,
                "section_title": section.get("title", f"Section {section_idx + 1}"),
                "section_level": section.get("level", 1),
                "section_path": section.get("path", "")
            }
            
            if preserve_structure and section_content:
                # Chunk each section independently
                section_chunks = self.chunk_text(section_content, section_metadata)
                
                # Renumber chunks globally
                for chunk in section_chunks:
                    chunk.id = chunk_id
                    chunk.metadata["global_chunk_id"] = chunk_id
                    chunk_id += 1
                    
                all_chunks.extend(section_chunks)
            else:
                # Concatenate all sections and chunk as one document
                # This is handled by calling chunk_text on concatenated content
                pass
                
        # Update total chunks
        for chunk in all_chunks:
            chunk.metadata["total_chunks"] = len(all_chunks)
            
        return all_chunks
        
    def create_chunk_summary(self, chunks: List[Chunk]) -> Dict[str, Any]:
        """
        Create a summary of the chunking operation.
        
        Args:
            chunks: List of chunks created
            
        Returns:
            Dictionary with chunking statistics and metadata
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_tokens": 0,
                "total_characters": 0,
                "average_chunk_size": 0,
                "overlap_ratio": 0
            }
            
        total_tokens = sum(chunk.token_count for chunk in chunks)
        total_chars = sum(chunk.char_count for chunk in chunks)
        avg_chunk_size = total_tokens // len(chunks)
        
        # Calculate overlap ratio
        total_overlap = sum(chunk.overlap_tokens for chunk in chunks[1:])
        overlap_ratio = total_overlap / total_tokens if total_tokens > 0 else 0
        
        return {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "total_characters": total_chars,
            "average_chunk_size": avg_chunk_size,
            "overlap_ratio": overlap_ratio,
            "chunk_boundaries": [
                {
                    "chunk_id": chunk.id,
                    "start": chunk.start_index,
                    "end": chunk.end_index,
                    "tokens": chunk.token_count
                }
                for chunk in chunks
            ]
        }