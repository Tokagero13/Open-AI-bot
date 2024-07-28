from test2 import global_thread_id, global_user_id
# from open_ai import 
import csv

global_thread_id 
global_user_id 

print(global_thread_id)
print(global_user_id)

def save_to_csv(id, global_user_id, global_thread_id):
    # Define the CSV file path
    csv_file = "data.csv"

    # Check if both global_thread_id and global_user_id are True
    if global_thread_id and global_user_id:
        # Open the CSV file in append mode
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the data to the CSV file
            writer.writerow([id, global_user_id, global_thread_id])
        
        print("Data saved to CSV file.")

# Example usage:
# Assuming global_thread_id and global_user_id are already defined
# and are boolean values indicating whether they are True or not
# Assuming id and global_user_id are also available

# Check if both global_thread_id and global_user_id are True
if global_thread_id and global_user_id:
    # Generate a unique id (you can use any method you prefer)
    # For simplicity, let's use an incrementing counter
    id = 1  # Example value

    # Save the data to the CSV file
    save_to_csv(id, global_user_id, global_thread_id)
else:
    print("global_thread_id or global_user_id is not True. Data not saved.")

