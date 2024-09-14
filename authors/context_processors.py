from authors.models import Author


def is_author(request):
    """ Context processor to check if the user is an author """
    # print(request.user)
    # if request.user.is_authenticated:
    #     print(request.user.id, Author.objects.filter(user__id=request.user.id))
    #     print(Author.objects.filter(user__id=request.user.id).exists())
    return {"is_author": request.user.is_authenticated and Author.objects.filter(user=request.user).exists()}