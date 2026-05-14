import re
from typing import Tuple, Optional

DANGEROUS_KEYWORDS = [
    'DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE',
    'ALTER', 'CREATE', 'REPLACE', 'EXEC', 'EXECUTE',
    'GRANT', 'REVOKE', 'LOCK', 'UNLOCK'
]


def validate_sql(sql: str) -> Tuple[bool, Optional[str]]:
    sql_upper = sql.strip().upper()
    
    if not sql_upper.startswith('SELECT'):
        return False, "SQL 语句必须以 SELECT 开头"
    
    for keyword in DANGEROUS_KEYWORDS:
        pattern = rf'\b{keyword}\b'
        if re.search(pattern, sql_upper):
            return False, f"SQL 语句包含危险操作关键字: {keyword}"
    
    return True, None