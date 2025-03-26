import streamlit as st
import requests
import json

class FunctionExecutionWebApp:
    def __init__(self, base_url="http://localhost:8000"):
        
        self.base_url = base_url
        self.session_id = None

    def execute_prompt(self, prompt, params=None):
        
        try:
            # Prepare request payload
            payload = {
                "prompt": prompt,
                "session_id": self.session_id
            }
            
            # Add parameters if provided
            if params:
                payload["params"] = params
            
            # Send request to API
            response = requests.post(f"{self.base_url}/execute", json=payload)
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                
                # Update session ID
                if result.get('session_id'):
                    self.session_id = result['session_id']
                
                return result
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
            return None

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Function Execution Interface", 
        page_icon="🤖",
        layout="wide"
    )
    
    # Create app instance
    app = FunctionExecutionWebApp()
    
    # Title and description
    st.title("🤖 Function Execution Interface")
    st.write("Execute system functions using natural language prompts")
    
    # Sidebar for additional controls
    st.sidebar.header("Function Execution Settings")
    
    # Main input area
    with st.form(key='prompt_form'):
        # Prompt input
        prompt = st.text_input("Enter your prompt", placeholder="Open Chrome, Check system resources, etc.")
        
        # Optional parameters
        use_params = st.checkbox("Add Parameters")
        params = None
        
        if use_params:
            params_input = st.text_area("Enter Parameters (JSON format)", height=100)
            try:
                params = json.loads(params_input) if params_input else None
            except json.JSONDecodeError:
                st.error("Invalid JSON format for parameters")
        
        # Submit button
        submit_button = st.form_submit_button("Execute")
    
    # Execute prompt when submitted
    if submit_button:
        if prompt:
            with st.spinner('Executing function...'):
                # Execute prompt
                result = app.execute_prompt(prompt, params)
                
                # Display result
                if result:
                    st.success("Function Executed Successfully!")
                    
                    # Tabs for different result views
                    tab1, tab2 = st.tabs(["Result", "JSON"])
                    
                    with tab1:
                        st.json(result)
                    
                    with tab2:
                        st.code(json.dumps(result, indent=2), language='json')
        else:
            st.warning("Please enter a prompt")
    
    # Additional information
    st.sidebar.info("""
    ### Supported Functions
    - Open Chrome
    - Open Calculator
    - Get System Resources
    - Run Shell Commands
    
    ### Tips
    - Use natural language prompts
    - Optional parameters can be added
    """)

if __name__ == "__main__":
    main()