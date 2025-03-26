from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from registry.function_registry import FunctionRegistry
from automation_functions.system_functions import SystemAutomation
from utils.session_manager import SessionManager
from utils.error_handler import ErrorHandler

class ExecutionRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    params: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    function: str
    result: Dict[str, Any]
    session_id: Optional[str] = None

# Create FastAPI app directly in routes
app = FastAPI()

# Initialize components
function_registry = FunctionRegistry()
system_automation = SystemAutomation()
session_manager = SessionManager()
error_handler = ErrorHandler()

@app.post("/execute")
async def execute_function(request: ExecutionRequest):
    try:
        # Manage session
        session_id = request.session_id or session_manager.create_session()
        
        # Find matching functions
        matched_functions = function_registry.search_functions(request.prompt)
        
        if not matched_functions:
            raise HTTPException(status_code=404, detail="No matching function found")
        
        # Get the first matched function
        function_name = matched_functions[0]
        
        # Get the function from SystemAutomation
        function = getattr(system_automation, function_name)
        
        # Execute function
        try:
            result = function(**request.params) if request.params else function()
            
            # Update session
            session_manager.update_session(
                session_id, 
                request.prompt, 
                function_name
            )
            
            return ExecutionResponse(
                function=function_name,
                result=result,
                session_id=session_id
            )
        
        except Exception as e:
            # Log function execution error
            error_handler.log_error(
                e, 
                context={
                    "function": function_name,
                    "prompt": request.prompt
                }
            )
            raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        # Global error handling
        error_handler.log_error(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurred")