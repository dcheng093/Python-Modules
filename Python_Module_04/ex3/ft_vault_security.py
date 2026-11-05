#!/usr/bin/env python3

def secure_archive(filename: str,
                   action: str = "read",
                   content: str = "") -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as f:
                data = f.read()
            return True, data
        elif action == "write":
            with open(filename, "w") as f:
                f.write(content)
            return True, "Content successfully written to file"
        else:
            return False, f"Invalid action '{action}'"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    print("=== Cyber Archives Security ===\n")
    result = secure_archive("/not/existing/file")
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(result)
    result = secure_archive("/etc/master.passwd")
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(result)
    result = secure_archive("ancient_fragment.txt")
    print("Using 'secure_archive' to read from a regular file:")
    print(result)
    if result[0]:
        write_result = secure_archive("new_fragment_from_security.txt",
                                      "write", result[1])
        print("\nUsing 'secure_archive' "
              "to write previous content to a new file:")
        print(write_result)

# print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
# print("Initiating secure vault access...")
# data = "classified_data.txt"
# security = "security_protocols.txt"
# print("Vault connection established with failsafe protocols\n")
# print("SECURE EXTRACTION:")
# with open(data, 'r') as f:
#     content = f.read()
#     print(content)
# print("\nSECURE PRESERVATION:")
# with open(security, 'r') as f:
#     content = f.read()
#     print(content)
# print("Vault automatically sealed upon completion\n")
# print("All vault operations completed with maximum security.")


# #!/usr/bin/python3.10

# def crisis_response(filename: str) -> None:
#     print(f"CRISIS ALERT: Attempting access to '{filename}'...")
#     try:
#         with open(filename, "r") as f:
#             content = f.read()
#     except FileNotFoundError:
#         print("RESPONSE: Archive not found in storage matrix")
#         print("STATUS: Crisis handled, system stable\n")
#         return
#     except PermissionError:
#         print("RESPONSE: Security protocols deny access")
#         print("STATUS: Crisis handled, security maintained\n")
#         return
#     print(f"ROUTINE ACCESS: Attempting access to '{filename}'...")
#     with open(filename, "r") as f:
#         content = f.read()
#         print(f"SUCCESS: Archive recovered - ''{content}''")
#         print("STATUS: Normal operations resumed\n")
#     print("All crisis scenarios handled successfully. Archives secure.")


# if __name__ == "__main__":
#     print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
#     crisis_response("lost_archive.txt")
#     crisis_response("classified_vault.txt")
#     crisis_response("standard_archive.txt")
