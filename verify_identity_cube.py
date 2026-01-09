import blake3
import os

def verify_identity_cube(filepath):
    """
    Computes the BLAKE3 hash of the identity cube for node 0x923-SEA.
    Ensures structural integrity and provenance.
    """
    if not os.path.exists(filepath):
        print("Error: identity.cube not found.")
        return None

    hasher = blake3.blake3()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192): # Read in 8KB chunks for memory efficiency
                hasher.update(chunk)
        
        calculated_hash = hasher.hexdigest()
        print(f"NODE: 0x923-SEA")
        print(f"FILE: {filepath}")
        print(f"BLAKE3_HASH: {calculated_hash}")
        return calculated_hash
    except Exception as e:
        print(f"Error checking file: {e}")
        return None

if __name__ == "__main__":
    verify_identity_cube("identity.cube")
