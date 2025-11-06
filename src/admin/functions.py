def css_for_table():
    css = """
    <style type="text/css" media="screen" style="width:100%">
        table, th, td {
            background-color: #0; 
            padding: 10px;
        }
        th {
            background-color: #0b0b0f; 
            shadow: 0 10px 30px rgba(0, 0, 0, 0.35); 
            color: white; 
            font-family: Tahoma;
            font-size : 13; 
            text-align: center;
        }
        td {
            background-color: #0b0b0f; 
            shadow:0 10px 30px rgba(0, 0, 0, 0.35); 
            color: white; 
            padding: 10px; 
            font-family: Calibri; 
            font-size : 12; 
            text-align: center;
        }
    </style>
    """
    return css