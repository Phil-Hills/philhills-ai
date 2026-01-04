def interleave_3d(x, y, d):
    """
    Computes the Z-Order (Morton Code) for 3D coordinates.
    Maps (x, y, d) to a single 1D index for locality preservation.
    """
    z = 0
    for i in range(32):
        z |= (x & 1 << i) << 2*i | (y & 1 << i) << (2*i + 1) | (d & 1 << i) << (2*i + 2)
    return hex(z)

if __name__ == "__main__":
    # Current Identity Mapping for Magnolia Lab
    # x: 476, y: 122, d: 0x923
    node_z = interleave_3d(476, 122, 2339) # 0x923 is 2339 in decimal
    print(f"Magnolia Lab Z-Index: {node_z}")
