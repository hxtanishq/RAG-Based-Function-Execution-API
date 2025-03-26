def test_imports():
    try:
        from api.routes import app
        print("API Routes imported successfully")
        
        from registry.function_registry import FunctionRegistry
        print("Function Registry imported successfully")
        
        from automation_functions.system_functions import SystemAutomation
        print("System Functions imported successfully")
        
        from utils.session_manager import SessionManager
        print("Session Manager imported successfully")
        
        from utils.error_handler import ErrorHandler
        print("Error Handler imported successfully")
        
    except ImportError as e:
        print(f"Import error: {e}")

if __name__ == "__main__":
    test_imports()