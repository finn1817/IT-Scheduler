import os
import shutil
import sys

def uninstall():
    try:
        # get rid of data directory and database
        if os.path.exists('data'):
            shutil.rmtree('data')
        
        print("Uninstallation completed successfully!")
        
    except Exception as e:
        print(f"An error occurred during uninstallation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    uninstall()
