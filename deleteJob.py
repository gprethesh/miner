import os
import shutil


def delete_jobid_folder_and_file(job_folder, jobid, filename):
    try:
        # Path to the jobid folder
        jobid_path = os.path.join(os.getcwd(), job_folder, jobid)

        # Verify the existence of the jobid folder
        if not os.path.exists(jobid_path):
            raise FileNotFoundError(
                f"The folder '{jobid}' does not exist in '{job_folder}'."
            )

        # Path to the file to be deleted
        file_path = os.path.join(jobid_path, filename)

        # Delete the file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {filename}")
        else:
            print(f"The file '{filename}' does not exist in '{jobid}'.")

        # Check if the jobid folder is empty, and delete it if it is
        if not os.listdir(jobid_path):  # List is empty, folder is empty
            shutil.rmtree(jobid_path)
            print(f"Deleted empty folder: {jobid}")
        else:
            print(f"Folder '{jobid}' is not empty, so it was not deleted.")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
