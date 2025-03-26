import os
import webbrowser
import psutil
import subprocess
from typing import Dict, Any

class SystemAutomation:
    @staticmethod
    def open_chrome(url: str = "https://www.google.com") -> Dict[str, Any]:
        
        try:
            webbrowser.open(url)
            return {
                "status": "success",
                "url": url,
                "message": f"Opened {url} in Chrome"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    @staticmethod
    def open_calculator() -> Dict[str, Any]:
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen("calc")
            elif os.name == 'posix':  # macOS/Linux
                subprocess.Popen(["gnome-calculator"])
            else:
                raise OSError("Unsupported operating system")
            
            return {
                "status": "success",
                "message": "Calculator opened successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    @staticmethod
    def get_system_resources() -> Dict[str, Any]:
         
        try:
            return {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    @staticmethod
    def run_shell_command(command: str) -> Dict[str, Any]:
         
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }