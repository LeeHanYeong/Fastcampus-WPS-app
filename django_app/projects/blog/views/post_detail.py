from django.shortcuts import get_object_or_404, render

from ..models import Post


def post_detail(request, pk):
    """
    post_detail뷰(지금 작업중인 뷰)에서 전달받은 pk를 이용해서
    pk값(id값)이 전달받은 pk인 Post객체를 Query하여 post라는 변수에 할당
    해당 변수를 render함수를 이용, post_detail.html템플릿을 이용해 리턴 (post변수는 'post'키로 전달되도록 한다)
    """
    # 아래와 같이 쓸 경우, pk값에 해당하는 Post객체가 존재하지 않을 경우
    # DoesNotExist에러 발생
    # post = Post.objects.get(pk=pk)

    # Post객체가 존재하지 않을 경우에는 404Error를 리턴해준다
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)