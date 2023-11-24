from rest_framework import authentication, exceptions, permissions

class ProductionAuthentication():
    authentication_classes = [authentication.TokenAuthentication]

class DebugSessionAuthentication():
    authentication_classes = [authentication.SessionAuthentication]

class DebugFullAuthentication():
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

class ViewOnlyOwnCompanyRestriction():
    def get_object(self):
        queryset = self.get_queryset()
        if self.request and self.request.user.id:
            obj = queryset.filter(id= self.request.user.company.id).first()
        else:
            raise exceptions.NotAuthenticated("Login with an authorized account")

        if not obj:
            raise exceptions.NotFound("No object found matching the specified lookup.")
        self.check_object_permissions(self.request, obj)
        return obj

class ViewOnlyOwnAccountRestriction():
    def get_object(self):
        queryset = self.get_queryset()
        if self.request and self.request.user.id:
            obj = queryset.filter(id= self.request.user.id).first()
        else:
            raise exceptions.NotAuthenticated("Login with an authorized account")

        if not obj:
            raise exceptions.NotFound("No object found matching the specified lookup.")
        self.check_object_permissions(self.request, obj)
        return obj



