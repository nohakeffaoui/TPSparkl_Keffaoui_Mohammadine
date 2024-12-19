import tkinter as tk
from tkinter import messagebox, scrolledtext
from SPARQLWrapper import SPARQLWrapper, JSON

# Function to execute SPARQL query
def execute_sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        messagebox.showerror("Error", f"Error executing query: {str(e)}")
        return None

# Function to display results in the output area
def display_results(results):
    if results:
        output_text.delete(1.0, tk.END)  # Clear previous output
        for result in results:
            for key, value in result.items():
                output_text.insert(tk.END, f"{key}: {value['value']}\n")
            output_text.insert(tk.END, "\n" + "-"*50 + "\n")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No results to display.")

# Function to handle query submission
def on_submit():
    query = query_text.get("1.0", tk.END).strip()  # Get the query from the text box
    if not query:
        messagebox.showwarning("Input Error", "Please enter a SPARQL query.")
        return

    results = execute_sparql_query(query)
    display_results(results)

# Create the main window
root = tk.Tk()
root.title("SPARQL Query Interface")

# Create a frame for the query input
query_frame = tk.Frame(root)
query_frame.pack(pady=10)

query_label = tk.Label(query_frame, text="Enter SPARQL Query:")
query_label.pack()

query_text = scrolledtext.ScrolledText(query_frame, wrap=tk.WORD, width=60, height=10)
query_text.pack()

# Create a submit button
submit_button = tk.Button(root, text="Submit Query", command=on_submit)
submit_button.pack(pady=10)

# Create a frame for the output display
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_label = tk.Label(output_frame, text="Results:")
output_label.pack()

# Create a scrolled text area for displaying the results
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=15)
output_text.pack()

# Run the Tkinter event loop
root.mainloop()