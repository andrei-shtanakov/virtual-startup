"""RAG (Retrieval Augmented Generation) Service using ChromaDB.

This service provides semantic search capabilities for the Creator agent
using vector embeddings and ChromaDB as the vector database.
"""

from typing import Any, Dict, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os


class RAGService:
    """Service for vector-based semantic search using ChromaDB."""

    def __init__(
        self,
        persist_directory: str = "./data/chromadb",
        collection_name: str = "knowledge_base",
    ):
        """Initialize the RAG service with ChromaDB.

        Args:
            persist_directory: Directory to persist the vector database
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
            ),
        )

        # Use default embedding function (sentence transformers)
        # For production, you might want to use OpenAI embeddings
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()

        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=collection_name, embedding_function=self.embedding_function
            )
        except Exception:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Knowledge base for virtual startup agents"},
            )

    def add_documents(
        self,
        documents: list[str],
        metadatas: Optional[list[Dict[str, Any]]] = None,
        ids: Optional[list[str]] = None,
    ) -> None:
        """Add documents to the knowledge base.

        Args:
            documents: List of text documents to add
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents (auto-generated if not provided)
        """
        if not documents:
            return

        # Generate IDs if not provided
        if ids is None:
            import uuid

            ids = [str(uuid.uuid4()) for _ in documents]

        # Add documents to collection
        self.collection.add(
            documents=documents, metadatas=metadatas or [{}] * len(documents), ids=ids
        )

    def search(
        self, query: str, k: int = 5, filter_metadata: Optional[Dict[str, Any]] = None
    ) -> list[Dict[str, Any]]:
        """Search for relevant documents using semantic similarity.

        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of result dictionaries with document, metadata, and distance
        """
        # Query the collection
        results = self.collection.query(
            query_texts=[query], n_results=k, where=filter_metadata
        )

        # Format results
        formatted_results = []

        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                result: Dict[str, Any] = {
                    "document": doc,
                    "metadata": results["metadatas"][0][i]
                    if results["metadatas"]
                    else {},  # type: ignore
                    "distance": results["distances"][0][i]
                    if results["distances"]
                    else 0.0,  # type: ignore
                    "id": results["ids"][0][i] if results["ids"] else None,  # type: ignore
                }
                formatted_results.append(result)

        return formatted_results

    def get_relevant_context(
        self, query: str, k: int = 5, max_chars: int = 2000
    ) -> str:
        """Get relevant context as a single string.

        Args:
            query: Search query
            k: Number of results to retrieve
            max_chars: Maximum characters to return

        Returns:
            Concatenated relevant documents
        """
        results = self.search(query, k=k)

        # Concatenate documents
        context_parts = []
        total_chars = 0

        for result in results:
            doc = result["document"]
            if total_chars + len(doc) > max_chars:
                # Truncate if needed
                remaining = max_chars - total_chars
                if remaining > 100:  # Only add if meaningful
                    context_parts.append(doc[:remaining] + "...")
                break

            context_parts.append(doc)
            total_chars += len(doc)

        return "\n\n---\n\n".join(context_parts)

    def delete_documents(self, ids: list[str]) -> None:
        """Delete documents from the knowledge base.

        Args:
            ids: List of document IDs to delete
        """
        if ids:
            self.collection.delete(ids=ids)

    def update_document(
        self,
        id: str,
        document: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update a document in the knowledge base.

        Args:
            id: Document ID
            document: New document text (optional)
            metadata: New metadata (optional)
        """
        update_data: Dict[str, Any] = {"ids": [id]}

        if document is not None:
            update_data["documents"] = [document]
        if metadata is not None:
            update_data["metadatas"] = [metadata]

        if len(update_data) > 1:  # More than just ids
            self.collection.update(**update_data)

    def count_documents(self) -> int:
        """Get the total number of documents in the knowledge base.

        Returns:
            Number of documents
        """
        return self.collection.count()

    def clear(self) -> None:
        """Clear all documents from the knowledge base."""
        # Delete the collection and recreate it
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "Knowledge base for virtual startup agents"},
        )

    def initialize_sample_data(self) -> None:
        """Initialize with sample knowledge for testing."""
        sample_docs = [
            "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including object-oriented, functional, and procedural programming.",
            "Flask is a lightweight WSGI web application framework in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.",
            "React is a JavaScript library for building user interfaces, particularly single-page applications. It was developed by Facebook and allows developers to create reusable UI components.",
            "AutoGen is a framework for building multi-agent AI systems. It enables the creation of conversational agents that can work together to solve complex tasks.",
            "Vector databases like ChromaDB enable semantic search by storing and querying vector embeddings of text. They are essential for Retrieval Augmented Generation (RAG) systems.",
            "TypeScript is a strongly typed programming language that builds on JavaScript. It adds optional static typing, classes, and interfaces to help catch errors during development.",
            "RESTful APIs are architectural style for designing networked applications. They use HTTP methods like GET, POST, PUT, and DELETE to perform CRUD operations on resources.",
            "SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a full suite of well-known enterprise-level persistence patterns.",
            "WebSocket is a computer communications protocol providing full-duplex communication channels over a single TCP connection. It enables real-time, bi-directional communication between clients and servers.",
            "CI/CD (Continuous Integration/Continuous Deployment) is a method to frequently deliver apps to customers by introducing automation into the stages of app development.",
        ]

        metadatas = [
            {"topic": "programming", "language": "python"},
            {"topic": "web_framework", "language": "python"},
            {"topic": "frontend", "language": "javascript"},
            {"topic": "ai", "category": "multi-agent"},
            {"topic": "database", "category": "vector"},
            {"topic": "programming", "language": "typescript"},
            {"topic": "architecture", "category": "api"},
            {"topic": "database", "language": "python"},
            {"topic": "networking", "category": "protocol"},
            {"topic": "devops", "category": "automation"},
        ]

        self.add_documents(documents=sample_docs, metadatas=metadatas)

        print(f"Initialized RAG service with {len(sample_docs)} sample documents")


# Global RAG service instance
_rag_service: Optional[RAGService] = None


def get_rag_service(
    persist_directory: str = "./data/chromadb", collection_name: str = "knowledge_base"
) -> RAGService:
    """Get or create the global RAG service instance.

    Args:
        persist_directory: Directory to persist the vector database
        collection_name: Name of the ChromaDB collection

    Returns:
        RAGService instance
    """
    global _rag_service

    if _rag_service is None:
        _rag_service = RAGService(
            persist_directory=persist_directory, collection_name=collection_name
        )

    return _rag_service

