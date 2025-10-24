"""
Installation and setup script for ThinkBuddy AI Assistant
This script helps verify the installation and setup of the AI assistant
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required_packages = [
        'fastapi',
        'chromadb',
        'google.generativeai',
        'sentence_transformers'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing.append(package)
    
    return missing

def install_dependencies(packages):
    """Install missing dependencies"""
    if not packages:
        return True
    
    print(f"\nInstalling missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'pip', 
            'install', 
            *packages
        ])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\nChecking environment configuration...")
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        print("⚠️  .env file not found")
        print("Creating .env template...")
        with open(env_path, 'w') as f:
            f.write("GEMINI_API_KEY=your_api_key_here\n")
        print("✅ .env template created. Please add your Gemini API key")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'GEMINI_API_KEY' not in content:
            print("⚠️  GEMINI_API_KEY not found in .env")
            return False
        if 'your_api_key_here' in content:
            print("⚠️  Please replace 'your_api_key_here' with your actual Gemini API key")
            return False
    
    print("✅ Environment configuration found")
    return True

def check_chroma_directory():
    """Check if ChromaDB directory exists"""
    print("\nChecking ChromaDB setup...")
    chroma_path = os.path.join(os.path.dirname(__file__), 'chroma_db')
    
    if os.path.exists(chroma_path):
        print(f"✅ ChromaDB directory exists at {chroma_path}")
    else:
        print(f"ℹ️  ChromaDB directory will be created on first run at {chroma_path}")
    
    return True

def test_imports():
    """Test if all services can be imported"""
    print("\nTesting service imports...")
    try:
        from app.services.chroma_service import chroma_service
        print("✅ ChromaDB service")
    except Exception as e:
        print(f"❌ ChromaDB service: {str(e)}")
        return False
    
    try:
        from app.services.assistant_service import assistant_service
        print("✅ Assistant service")
    except Exception as e:
        print(f"❌ Assistant service: {str(e)}")
        return False
    
    try:
        from app.routes.assistant_routes import router
        print("✅ Assistant routes")
    except Exception as e:
        print(f"❌ Assistant routes: {str(e)}")
        return False
    
    return True

def main():
    """Main installation check"""
    print("=" * 60)
    print("ThinkBuddy AI Assistant - Installation Checker")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        response = input("\nInstall missing packages? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies(missing):
                return
        else:
            print("⚠️  Please install missing packages manually:")
            print(f"   pip install {' '.join(missing)}")
            return
    
    # Check environment
    env_ok = check_env_file()
    
    # Check ChromaDB
    check_chroma_directory()
    
    # Test imports
    imports_ok = test_imports()
    
    # Summary
    print("\n" + "=" * 60)
    print("Installation Summary")
    print("=" * 60)
    
    if env_ok and imports_ok:
        print("✅ All checks passed! The AI Assistant is ready to use.")
        print("\nNext steps:")
        print("1. Start the backend server: python main.py")
        print("2. Access the assistant through the frontend")
        print("3. Check API documentation: http://127.0.0.2:8000/docs")
    else:
        print("⚠️  Some issues need attention:")
        if not env_ok:
            print("   - Configure GEMINI_API_KEY in .env file")
        if not imports_ok:
            print("   - Fix import errors shown above")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
