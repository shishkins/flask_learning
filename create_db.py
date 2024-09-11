

if __name__ == '__main__':
    from app import app, db
    import os
    if not os.path.exists('/instance/blog.db'):
        app.app_context().push()
        db.create_all()