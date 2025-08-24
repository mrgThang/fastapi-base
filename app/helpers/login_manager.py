from fastapi import HTTPException, Depends

def login_required():
    return True


class PermissionRequired:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self):
        self.user = user
        if self.user.role not in self.permissions and self.permissions:
            raise HTTPException(status_code=400,
                                detail=f'User {self.user.email} can not access this api')
