import os
import shutil

def uninstall():
    try:
        # remove the data directory and all of its stuff w it
        if os.path.exists('data'):
            shutil.rmtree('data')
            print("Database and data directory removed successfully")
        else: # if directory isnt found
            print("Data directory not found")
            # for successful uninstal...
        print("Uninstallation complete!")
        # if error print this
    except Exception as e:
        print(f"An error occurred during uninstallation: {str(e)}")

if __name__ == "__main__":
    uninstall()
