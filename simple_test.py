"""
Simple standalone test without dependencies
"""

import sys
import os
sys.path.append('src')

# Test basic imports
try:
    print("Testing basic Python functionality...")
    import asyncio
    import json
    from datetime import datetime
    print("✅ Basic imports successful")
    
    # Test if our files exist
    if os.path.exists('src/agent.py'):
        print("✅ Agent file exists")
    else:
        print("❌ Agent file missing")
    
    if os.path.exists('src/evaluation.py'):
        print("✅ Evaluation file exists")
    else:
        print("❌ Evaluation file missing")
    
    if os.path.exists('src/cli.py'):
        print("✅ CLI file exists")
    else:
        print("❌ CLI file missing")
    
    print("\n📁 Project Structure:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if not file.startswith('.'):
                print(f"{subindent}{file}")
    
    print("\n🎉 PROJECT STRUCTURE VERIFICATION COMPLETE!")
    print("\nNext steps:")
    print("1. Install dependencies: pip3 install -r requirements.txt")
    print("2. Set up HuggingFace token in .env file")
    print("3. Run: python3 src/cli.py --help")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
