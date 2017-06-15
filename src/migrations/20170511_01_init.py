"""

"""

from yoyo import step

__depends__ = {}

CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS todo (
    id SERIAL,
    title varchar not null,
    description varchar not null default '',
    created_at timestamp not null,
    updated_at timestamp not null
);
'''

DROP_TABLE = '''
DROP TABLE IF EXISTS todo;
'''

steps = [
    step(CREATE_TABLE)
]
