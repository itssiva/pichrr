def txt2set(text):
    """
    Will be converted into a space-delimited string set
    """
    return set([element.strip().lower() for element in text.split(',') if element.strip() != ''])


def is_superuser(user):
    return user.is_authenticated() and user.is_superuser


def get_count(sql, params):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql, params)
    count=0
    for row in cursor.fetchall():
        count=row[0]
    return count
