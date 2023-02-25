async def get_desh_args(text: str) -> dict:
    """
    {key: value, key: values} 
     
    key-values--key-values
    """
    return {x.split('-')[0]: int(x.split('-')[1]) for x in text.split('--')}