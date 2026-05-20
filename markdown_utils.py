def dataframe_to_markdown(df, index=False):
    if index:
        df = df.reset_index()
    df = df.copy()
    headers = [str(col) for col in df.columns]
    rows = [[str(value) for value in row] for row in df.to_numpy()]
    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]

    def fmt_row(values):
        return '| ' + ' | '.join(str(value).ljust(width) for value, width in zip(values, widths)) + ' |'

    separator = '| ' + ' | '.join('-' * width for width in widths) + ' |'
    return '\n'.join([fmt_row(headers), separator] + [fmt_row(row) for row in rows])
