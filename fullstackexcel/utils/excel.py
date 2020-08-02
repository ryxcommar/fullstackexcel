import re

from typing import Union
from typing import Type
from typing import Optional
from typing import List
from typing import Dict
from typing import Any
import pandas as pd


def sheets_in_workbook(excel_file: str):
    return pd.ExcelFile(excel_file).sheet_names


def load_simple(
        excel_file: str,
        sheet_name: Optional[str] = None,
        return_type: Optional[Type] = None
) -> Union[Dict[str, str], List[str]]:
    """
    This function does a simple load of a worksheet, which loads a 1-column
    sheet as a list, a 2-column sheet as a dict, and raises a TypeError either
    if there are not 1-2 columns, or if the return_type doesn't correspond with
    the requisite number of columns.

    ``sheet_name`` is optional if using the ``[wb.xlsx]sheet_name`` convention,
    or if there is only one sheet in a workbook. That said, it's still
    recommended that you pass in a worksheet using ``sheet_name``.

    :param excel_file:
    :param sheet_name:
    :param return_type:
    :return:
    """
    if sheet_name is None:
        regex = re.match('\[(.*?\.xls[x]?)\](.+)', excel_file)
        if regex:
            excel_file = regex[1]
            sheet_name = regex[2]
        else:
            sheets = sheets_in_workbook(excel_file)
            if len(sheets == 1):
                sheet_name = sheets[0]
            else:
                raise ValueError('You need to specify a worksheet to load.')
    df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    if len(df.columns) == 1 and return_type in [list, 'list', None]:
        return list(df[0])
    elif len(df.columns) == 2 and return_type in [dict, 'dict', None]:
        return dict(zip(*map(list, [df[0], df[1]])))
    else:
        # Prepare the error message.
        cols = {
            list: '1 column',
            'list': '1 column',
            dict: '2 columns',
            'dict': '2 columns',
            None: 'between 1 and 2 columns'
        }
        actual = f'{len(df)} column' if len(df) == 1 else f'{len(df)} columns.'
        raise TypeError(f'The sheet {sheet_name} must contain {cols}. However, '
                        f'it contains {actual}.')


def build_workbook_from_dict(data: Dict[str, List[List[Any]]], file_name: str):
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        kwargs = {
            'excel_writer': writer,
            'header': False,
            'index': False
        }
        for sheet_name, d in data.items():
            pd.DataFrame(d).to_excel(sheet_name=sheet_name, **kwargs)
