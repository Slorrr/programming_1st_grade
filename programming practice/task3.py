import csv
import pickle
import os

def load_table_from_file(filename):
    """Load table data from a given file."""
    _, ext = os.path.splitext(filename)
    if ext == '.csv':
        return _load_csv(filename)
    elif ext == '.pkl':
        return _load_pickle(filename)
    else:
        raise ValueError('Unsupported file format.')

def _load_csv(filename):
    """Load table data from a CSV file."""
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        table = list(reader)
        return {'attributes': {'delimiter': ','}, 'data': table}

def _load_pickle(filename):
    """Load table data from a pickle file."""
    with open(filename, 'rb') as file:
        table = pickle.load(file)
        return {'attributes': {'format': 'pickle'}, 'data': table}

def save_table_to_file(table, filename):
    """Save table data to a given file format."""
    _, ext = os.path.splitext(filename)
    if ext == '.csv':
        _save_csv(table, filename)
    elif ext == '.pkl':
        _save_pickle(table, filename)
    elif ext == '.txt':
        _save_text(table, filename)
    else:
        raise ValueError('Unsupported file format.')

def _save_csv(table, filename):
    """Save table data to a CSV file."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table['data'])

def _save_pickle(table, filename):
    """Save table data to a pickle file."""
    with open(filename, 'wb') as file:
        pickle.dump(table['data'], file)

def _save_text(table, filename):
    """Save table data to a text file."""
    with open(filename, 'w') as file:
        for row in table['data']:
            file.write(' '.join(map(str, row)) + '\n')

def get_rows_by_number(table, start, stop=None, copy_table=False):
    """Get rows by number range."""
    if stop is None:
        stop = start + 1
    data = table['data'][start:stop]
    return {'attributes': table['attributes'], 'data': data[:] if copy_table else data}

def get_rows_by_index(table, *values, copy_table=False):
    """Get rows by index values."""
    indices = [i for i, row in enumerate(table['data']) if row[0] in values]
    data = [table['data'][i] for i in indices]
    return {'attributes': table['attributes'], 'data': data[:] if copy_table else data}

def get_column_types(table, by_number=True):
    """Get types of columns in the table."""
    column_types = {}
    for i, column in enumerate(table['data'][0]):
        column_types[i if by_number else column] = type(column).__name__
    return column_types

def set_column_types(table, types_dict, by_number=True):
    """Set types of columns in the table."""
    column_types = get_column_types(table, by_number=by_number)
    for column, value_type in types_dict.items():
        if column not in column_types:
            raise ValueError('Invalid column.')
        if column_types[column] != value_type:
            for i, row in enumerate(table['data']):
                row[column if by_number else row.index(column)] = value_type(row[column if by_number else row.index(column)])

def get_values(table, column=0):
    """Get values from a specified column."""
    return [row[column] for row in table['data']]

def get_value(table, column=0):
    """Get a single value from a specified column."""
    if len(table['data']) != 1:
        raise ValueError('The table should contain only one row.')
    return table['data'][0][column]

def set_values(table, values, column=0):
    """Set values in a specified column."""
    if len(values) != len(table['data']):
        raise ValueError('Length of values does not match number of rows.')
    for i, row in enumerate(table['data']):
        row[column] = values[i]

def set_value(table, value, column=0):
    """Set a single value in a specified column."""
    if len(table['data']) != 1:
        raise ValueError('The table should contain only one row.')
    table['data'][0][column] = value

def print_table(table):
    """Print the table."""
    for row in table['data']:
        print(' '.join(map(str, row)))

def check_file_format(filename):
    """Check if file format is supported."""
    _, ext = os.path.splitext(filename)
    if ext not in ['.csv', '.pkl', '.txt']:
        raise ValueError('Unsupported file format.')

def check_column(table, column, by_number=True):
    """Check if column is valid."""
    if by_number:
        if column not in range(len(table['data'][0])):
            raise ValueError('Invalid column number.')
    else:
        if column not in table['data'][0]:
            raise ValueError('Invalid column name.')

def check_table_length(table, expected_length):
    """Check if table length is as expected."""
    if len(table['data']) != expected_length:
        raise ValueError('Invalid table length.')
