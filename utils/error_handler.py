import logging
import traceback
from typing import Dict, Any, Optional

class ErrorHandler:
    def __init__(self, log_file: str = 'function_execution.log'):
        
        # Configure logging
        logging.basicConfig(
            
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
         
        self.error_stats = {
            "total_errors": 0,
            "error_types": {}
        }

    def log_error(self, 
                  error: Exception, 
                  context: Optional[Dict[str, Any]] = None,
                  severity: str = 'ERROR'):
      
        self.error_stats['total_errors'] += 1
        
        # Track error types
        error_type = type(error).__name__
        self.error_stats['error_types'][error_type] = \
            self.error_stats['error_types'].get(error_type, 0) + 1
        
        # Detailed logging
        error_details = {
            "error_type": error_type,
            "error_message": str(error),
            "traceback": traceback.format_exc()
        }
         
        if context:
            error_details['context'] = context
         
        log_method = getattr(self.logger, severity.lower())
        log_method(f"Error Details: {error_details}")

    def get_error_stats(self) -> Dict:
         
        return self.error_stats