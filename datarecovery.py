import os

def recover_files(drive, signature, output_dir):
    with open(drive, "rb") as fileD:
        size = 512
        byte = fileD.read(size)
        offset = 0
        file_count = 0

        while byte:
            found = byte.find(signature)
            while found >= 0:
                # File signature found, start carving the file
                file_name = f"recovered_file_{file_count}.dat"
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, "wb") as fileN:
                    fileN.write(byte[found:])

                    while True:
                        byte = fileD.read(size)
                        bfind = byte.find(signature)
                        if bfind >= 0:
                            # Another file signature found, write the remaining bytes and continue carving
                            fileN.write(byte[:bfind])
                            break
                        else:
                            fileN.write(byte)

                    print(f"Recovered file: {file_name}")
                    file_count += 1

                found = byte.find(signature, found + 1)

            byte = fileD.read(size)
            offset += 1

# Example usage
drive_path = r"\\.\G:"  # Path to the drive or file you want to recover data from
output_directory = "recovered_files"  # Directory to store the recovered files
signature = b"\xff\xd8\xff\xe0\x00\x10\x4a\x46"  # Signature for JPEG files

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

recover_files(drive_path, signature, output_directory)
