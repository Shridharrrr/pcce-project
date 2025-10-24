"""
Quick test script to diagnose ThinkBuddy AI Assistant issues
Run this to check if the backend is working correctly
"""

import sys
import os

print("=" * 60)
print("ThinkBuddy AI Assistant - Diagnostic Test")
print("=" * 60)

# Test 1: Check imports
print("\n[1/5] Testing imports...")
try:
    import chromadb
    print("✅ chromadb imported")
except ImportError as e:
    print(f"❌ chromadb import failed: {e}")
    print("   Fix: pip install chromadb")
    sys.exit(1)

try:
    import google.generativeai as genai
    print("✅ google.generativeai imported")
except ImportError as e:
    print(f"❌ google.generativeai import failed: {e}")
    print("   Fix: pip install google-generativeai")
    sys.exit(1)

try:
    from sentence_transformers import SentenceTransformer
    print("✅ sentence-transformers imported")
except ImportError as e:
    print(f"❌ sentence-transformers import failed: {e}")
    print("   Fix: pip install sentence-transformers")
    sys.exit(1)

# Test 2: Check environment
print("\n[2/5] Checking environment...")
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyArgXw1-BZKu-dXdbXr_CfNrPiB4eoUEcw")
if GEMINI_API_KEY and GEMINI_API_KEY != "your_api_key_here":
    print(f"✅ GEMINI_API_KEY found: {GEMINI_API_KEY[:10]}...")
else:
    print("⚠️  GEMINI_API_KEY not properly configured")

# Test 3: Test ChromaDB service
print("\n[3/5] Testing ChromaDB service...")
try:
    from app.services.vector_db_service import (
        add_message_to_vector_db, 
        search_relevant_context,
        get_collection_stats
    )
    print("✅ Vector DB service imported")
    
    # Test adding and searching
    test_id = "test_message_001"
    success = add_message_to_vector_db(
        message_id=test_id,
        content="This is a test message about project planning and development",
        metadata={
            "team_id": "test_team",
            "sender_name": "Test User",
            "message_type": "text",
            "timestamp": "2025-01-01T00:00:00"
        }
    )
    if success:
        print("✅ Can write to Vector DB")
    
    results = search_relevant_context("project planning", team_id="test_team", n_results=1)
    if results:
        print(f"✅ Can search Vector DB - Found {len(results)} results")
    
    stats = get_collection_stats()
    print(f"✅ Vector DB stats: {stats}")
    print("✅ ChromaDB fully functional")
    
except Exception as e:
    print(f"❌ ChromaDB service error: {e}")
    print("   This might be the issue!")
    import traceback
    traceback.print_exc()

# Test 4: Test Gemini API
print("\n[4/5] Testing Gemini API...")
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'Hello' in one word")
    if response and response.text:
        print(f"✅ Gemini API working: {response.text.strip()}")
    else:
        print("⚠️  Gemini API returned empty response")
except Exception as e:
    print(f"❌ Gemini API error: {e}")
    print("   Check your API key or network connection")
    import traceback
    traceback.print_exc()

# Test 5: Test Assistant service
print("\n[5/5] Testing Assistant service...")
try:
    from app.services.assistant_service import assistant_service
    print("✅ Assistant service initialized")
    
    # Try to generate a response
    import asyncio
    
    async def test_response():
        result = await assistant_service.generate_response(
            user_id="test_user",
            message="Hello, this is a test",
            project_context=None,
            use_rag=False  # Disable RAG for quick test
        )
        return result
    
    result = asyncio.run(test_response())
    if result and result.get('response'):
        print(f"✅ Assistant generated response: {result['response'][:50]}...")
        print("✅ Assistant service fully functional!")
    else:
        print("⚠️  Assistant returned empty response")
        
except Exception as e:
    print(f"❌ Assistant service error: {e}")
    print("   This is likely the issue!")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 60)
print("Diagnostic Summary")
print("=" * 60)
print("\nIf all tests passed (✅), the backend should work correctly.")
print("If any test failed (❌), fix the issue and run this script again.")
print("\nTo start the server:")
print("  python main.py")
print("\nTo test the API endpoint:")
print("  curl http://127.0.0.1:8000/api/assistant/health")
print("=" * 60)
