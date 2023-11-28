import openai
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests
import os
#OpenAI API key
openai.api_key = "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"


# GitHub credentials
github_username = "RKPratibha"
github_token = "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"
repository_name = "MDS2"
file_path = "Store_Project_X" 
class Kernel:
    def __init__(self):
        self.user_input = None
        self.generated_code = None

    def process_user_request(self, user_input):
        # Process user request, interact with GPT-3, and store the generated code
        self.user_input = user_input
        user_input = os.environ.get("USER_INPUT")
        # Use user_input in your script

        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=self.user_input,
                max_tokens=850
            )
            self.generated_code = response.choices[0].text
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def execute_code(self):
        # Execute the generated code locally and get output
        if self.generated_code:
            try:
                result = subprocess.run(['python', '-c', self.generated_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                return result.stdout, result.stderr
            except Exception as e:
                return None, str(e)
        else:
            return None, "No code to execute."

# Function to push data to GitHub
def push_to_github(user_input, generated_code,github_token,github_username,repository_name, file_path):
    #github_api_url = f"https://github.com/RKPratibha/MDS2.git"
    github_api_url = f"https://api.github.com/repos/RKPratibha/MDS2/contents/Store_Project_X?ref=main"
    commit_message = f"Update generated information for: {user_input}"

    headers = {
          "Accept": "application/vnd.github+json",
          "Authorization": f"Bearer {github_token}",
          "X-GitHub-Api-Version": "2022-11-28"
        
        }
    try:
        # Retrieve current file details
        response = requests.get(github_api_url, headers=headers)
        response.raise_for_status()
        current_content = response.json().get("content", "")
        current_sha = response.json().get("sha", "")

        # Encode the new content (user_input + generated_code) to base64
        import base64
        new_content = base64.b64encode(f"User Input: {user_input}\nGenerated Code:\n{generated_code}".encode()).decode()

        # If the content has changed, update the file on GitHub
        if new_content != current_content:
            data = {
                "message": f"Update generated information for: {user_input}",
                "content": new_content,
                "sha": current_sha
            }

            # Make the PUT request to update the file
            response = requests.put(github_api_url, json=data, headers=headers)
            response.raise_for_status()

            print("Successfully pushed to GitHub.")
            return True
        else:
            print("Content has not changed. No update needed.")
            return False

    except Exception as e:
        print(f"GitHub Push Error: {str(e)}")
        return False

# Usage
user_input = os.environ.get("USER_INPUT")
generated_code = "Your generated code here"
github_username = "RKPratibha"
github_token = "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"
repository_name = "MDS2"
file_path = "Store_Project_X" 

# Call the function to push to GitHub
push_result = push_to_github(user_input, generated_code,github_token, github_username, repository_name, file_path)

if push_result:
    print("Generated information pushed to GitHub successfully!")
else:
    print("Failed to push to GitHub.")
    
 

# Class for the GUI
class GUI:
    def __init__(self, root, kernel):
        self.root = root
        self.kernel = kernel

        self.root.title("Project X - AI Assisted Systems Engineering")

        self.user_input_label = tk.Label(root, text="Enter your request:")
        self.user_input_entry = tk.Entry(root, width=60)
        self.generate_button = tk.Button(root, text="Generate Response", command=self.generate_response, bg="blue", fg="white")
        self.execute_button = tk.Button(root, text="Execute Code", command=self.execute_code, bg="green", fg="white")
        self.github_button = tk.Button(root, text="Push to GitHub", command=self.push_to_github, bg="orange", fg="white")
        self.output_text = tk.Text(root, height=20, width=80)

        self.user_input_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        self.user_input_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
        self.generate_button.grid(row=2, column=0, padx=10, pady=10)
        self.execute_button.grid(row=2, column=1, padx=10, pady=10)
        self.github_button.grid(row=2, column=2, padx=10, pady=10)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def generate_response(self):
        user_input = self.user_input_entry.get()
        if user_input:
            self.kernel.process_user_request(user_input)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, self.kernel.generated_code)
        else:
            messagebox.showwarning("Warning", "Please enter a prompt.")

    def execute_code(self):
        stdout, stderr = self.kernel.execute_code()
        self.output_text.delete(1.0, tk.END)
        if stdout:
            self.output_text.insert(tk.END, "Output:\n" + stdout)
        if stderr:
            self.output_text.insert(tk.END, "Error:\n" + stderr)

    def push_to_github(self):
        user_input = self.user_input_entry.get()
        generated_code = self.kernel.generated_code
        if user_input and generated_code:
            # GitHub credentials
            github_username = "RKPratibha"
            #github_token = "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"
            github_token = "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"
            
            github_push_result = push_to_github(user_input, generated_code,github_token, github_username,repository_name, file_path)
            if github_push_result:
                messagebox.showinfo("GitHub Push", "Generated information pushed to GitHub successfully!")
            else:
                messagebox.showerror("GitHub Push", "Failed to push to GitHub.")
        else:
            messagebox.showwarning("Warning", "Please generate information before pushing to GitHub.")

if __name__ == "__main__":
    root = tk.Tk()
    kernel = Kernel()
    gui = GUI(root, kernel)

    root.mainloop()
