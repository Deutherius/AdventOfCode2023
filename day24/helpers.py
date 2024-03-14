class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BCKGGREEN = '\x1b[6;30;42m'
    BCKRED = '\x1b[0;31;41m'
    ENDBCKG = '\x1b[0m'
    ENDC = '\033[0m'

def pad(matrix, pad_element, padding_size):
    """
    Pad the matrix with the specified element and size.

    Parameters:
    - matrix: The input matrix (list of strings or list of lists).
    - pad_element: The element to use for padding (must be a single character for strings).
    - padding_size: The number of padded rows and columns.

    Returns:
    - The padded matrix.
    """
    if all(isinstance(row, str) for row in matrix):
        # Check if pad_element is a single character
        if not (isinstance(pad_element, str) and len(pad_element) == 1):
            raise ValueError("For strings, pad_element must be a single character.")

        # If it's a list of strings, pad each string in each row
        padded_matrix = [pad_element * padding_size + elem + pad_element * padding_size for elem in matrix]

        # Pad the top and bottom of the matrix
        padding_row = pad_element * len(padded_matrix[0])
        padded_matrix = [padding_row] * padding_size + padded_matrix + [padding_row] * padding_size
    elif all(isinstance(row, list) for row in matrix):
        # If it's a list of lists, pad each row in the matrix
        # Check if pad_element is a single element (not a list)
        if isinstance(pad_element, list) and len(pad_element) != 1:
            raise ValueError("For lists, pad_element must be a single element (not a list).")

        padding_row = [pad_element] * (len(matrix[0]) + 2 * padding_size)
        padded_matrix = [padding_row] * padding_size + [[pad_element] * padding_size + row + [pad_element] * padding_size for row in matrix] + [padding_row] * padding_size
    else:
        raise ValueError("Unsupported matrix format. Use a list of strings or a list of lists.")

    return padded_matrix

def repmat(matrix, repetitions):
    """
    Repeat the matrix the specified number of times along each axis.

    Parameters:
    - matrix: The input matrix (list of strings or list of lists).
    - repetitions: The number of times to repeat the matrix along each axis.

    Returns:
    - The repeated matrix.
    """
    # Check if the input is a list of strings or a list of lists
    if all(isinstance(row, str) for row in matrix):
        # If it's a list of strings, repeat each string in each row
        repeated_matrix = [elem * repetitions[1] for elem in matrix] * repetitions[0]
    elif all(isinstance(row, list) for row in matrix):
        # If it's a list of lists, repeat each row in the matrix
        repeated_matrix = [row * repetitions[1] for row in matrix] * repetitions[0]
    else:
        raise ValueError("Unsupported matrix format. Use a list of strings or a list of lists.")

    return repeated_matrix

def printArray(arr):
    def is_1d_array(array):
        return isinstance(array, (str, list)) and all(isinstance(elem, (int, float, str)) for elem in array)

    def is_2d_array(array):
        return isinstance(array, list) and all(is_1d_array(row) for row in array)

    def is_3d_array(array):
        return isinstance(array, list) and all(is_2d_array(matrix) for matrix in array)

    def print_1d_array(array):
        print(array)

    def print_2d_array(array):
        if all(isinstance(elem, str) for elem in array[0]):
            max_width = max(len(elem) for row in array for elem in row)
            for row in array:
                print([f"{elem:<{max_width}}" for elem in row])
        else:
            column_widths = [max(len(str(elem)) for elem in col) for col in zip(*array)]
            for row in array:
                print([f"{elem:>{width}}" for elem, width in zip(row, column_widths)])

    def print_3d_array(array):
        for i, matrix in enumerate(array):
            print(f"submatrix {i}:")
            print_2d_array(matrix)
            print()
            

    if is_1d_array(arr):
        print_1d_array(arr)
    elif is_2d_array(arr):
        print_2d_array(arr)
    elif is_3d_array(arr):
        print_3d_array(arr)
    else:
        print("Invalid input type")