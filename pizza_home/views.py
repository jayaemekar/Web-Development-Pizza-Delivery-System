from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,Http404
from .decorators import *
from .models import *

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def index(request):
    try:
        user = request.user    
        user = user.get_full_name()  
    except:
        user = 'Anonymous User'

    pizza = Pizza.objects.all()
    total_pizza_num = len(pizza)
    pizza_paginator = Paginator(pizza, 4)
    pizza_page = request.GET.get('page')
    paginated_pizza_list_query = pizza_paginator.get_page(pizza_page)
    
    context = {
        'title': 'Cal Pizza Delivery System',     
        'user': user,
        'pizzas': paginated_pizza_list_query,
        'total_pizza_num': total_pizza_num,
    }
    return render(request, 'pizza_home/index.html', context)

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def order(request, order_id):
    try:
        user = request.user  
        user = user.get_full_name() 
    except:
        user = 'Anonymous User'
    order = Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('pizza_home:homepage')
    context = {
        'title': 'Pizza App: Order Status Page',
        'order': order,
        'user': user,
    }
    return render(request, 'pizza_home/order.html', context)

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def order_list(request):
    try:
        user = request.user 
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    order = Order.objects.order_by('-id').filter(user_id=request.user.id)   # display the latest orders
    total_order_num = len(order)
    order_paginator = Paginator(order, 5)
    order_page = request.GET.get('page')
    paginated_order_list_query = order_paginator.get_page(order_page)
    context = {
        'title': 'Orders List',
        'user': user,
        'orders': paginated_order_list_query,
        'total_order_num': total_order_num,
    }

    return render(request, 'pizza_home/order_list.html', context)



def error_404_view(request, exception):
    return render(request, '404_page_not_found.html')

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def room(request):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'
    context = {
        'user': user,
    }
    return render(request, 'pizza_home/room.html', context)

def about_view(request):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    context = {
        'user': user,
    }
    return render(request , 'pizza_home/about.html',context)


def contactus_view(request):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    context = {
        'user': user,
    }
    return render(request , 'pizza_home/contactus.html',context)

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def show_pizza_record(request,name):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    pizza = Pizza.objects.filter(name=name).first()
  
    reviews = Review.objects.filter(restaurant=pizza).order_by("-pk")

    avg_rate = average_rating(reviews)
    context = {
        'user': user,
        'pizza': pizza,
        'name': name,
        'reviews': reviews,
        'avg_rate': avg_rate,
    }
    return render(request , 'pizza_home/show_pizza_record.html',context)

@csrf_exempt
@stop_restaurant_staff
def order_pizza(request):
    # return JsonResponse({ 'testing': 'Success' }) # testing API

    try:
        print("Test",request.user)
        print(json.loads(request.body))
        
        # fetching data send from the frontend func ("createOrder")
        user = request.user # fetch user info from 'index.html'
      
        data = json.loads(request.body) # fetch all the django-vars from 'index.html', especially focuses on 'pizza' information. Converts a JSON-obj to a python-dictionary.
        
        print("Test",user)
        pizza = Pizza.objects.get(id=data.get('id'))    # extract the specific pizza-obj from db using the 'pizza.id' onclick 'createOrder({{p.id}})' func existed in 'index.html'
        
        # [ INSERT RECORD TO DB ]
        # Creating an single-record in the 'Order' model-class
        order = Order(user=user, pizza=pizza, amount=pizza.price)
        order.save()

        return JsonResponse({ 'status': True, 'message': 'Success', 'order': 'A new order is created' })
    except:
        return JsonResponse({ 'status': False, 'error': 'Something went wrong' })




def average_rating(reviews):
    avg_rating = 0
    if reviews.count() > 0:
        total = 0
        for review in reviews:
            total += review.rate
        avg_rating = total/reviews.count()
        return "{0:.2f}".format(avg_rating)
    else:
        return avg_rating


@login_required
def like_review(request):
    review_id = request.GET.get('review_id')
    preference = request.GET.get('preference')

    # [0]: unlike [1]:like
    if preference == "0":
        LikeForReview.objects.filter(
            review_id=review_id, user=request.user).delete()
        count = LikeForReview.objects.filter(review_id=review_id).count()
        return JsonResponse({'count': count, }, status=200)
    elif preference == "1":

        bExist = LikeForReview.objects.filter(
            review_id=review_id, user=request.user).exists()

        if not bExist:
            lr1 = LikeForReview(review_id=review_id, user=request.user)
            lr1.save()
            count = LikeForReview.objects.filter(review_id=review_id).count()
            response = JsonResponse({
                'status': 'succeeded ',
                'message': lr1.id,
                'count': count,
            }, status=200)
            return response

    response = JsonResponse({
        'status': 'failed',
        'message': 'LikeForReview sqlite exception',
    }, status=500)
    return response


@login_required
def like_comment(request):
    comment_id = request.GET.get('comment_id')
    preference = request.GET.get('preference')
    user = request.user

    # preference [0]:Unlike [1]:like
    if preference == "0":
        LikeForComment.objects.filter(
            comment_id=comment_id, user=user).delete()
        count = LikeForComment.objects.filter(comment_id=comment_id).count()

        return JsonResponse({'count': count, }, status=200)

    elif preference == "1":
        bExist = LikeForComment.objects.filter(
            comment_id=comment_id, user=user).exists()

        if not bExist:
            lc1 = LikeForComment(comment_id=comment_id, user=user)
            lc1.save()
            count = LikeForComment.objects.filter(
                comment_id=comment_id).count()

            response = JsonResponse({
                'status': 'succeeded',
                'message': lc1.id,
                'count': count,
            }, status=200)
            return response

    response = JsonResponse({
        'status': 'failed',
        'message': '',
    }, status=500)
    return response


def review_create(request):
    if request.user.is_authenticated:
        restaurant_id = request.GET.get("restaurant_id")
        description = request.GET.get("description")
        rate = request.GET.get("rate")

        review = Review(
            user=request.user,
            restaurant_id=restaurant_id,
            rate=int(rate),
            description=description
        )
        review.save()

        reviews = Review.objects.filter(
            restaurant_id=restaurant_id).order_by("-pk")

        content = {
            "reviews": reviews
        }

        return render(request, "pizza_home/review.html", content)

        # return JsonResponse({"review_id": review.id}, status=200)
    else:
        return JsonResponse({"is_not_authenticated": True}, status=200)


def comment_create(request):
    if request.user.is_authenticated:
        review_id = request.GET.get("review_id")
        comment_id = request.GET.get("comment_id")
        description = request.GET.get("description")

        review = Review.objects.filter(id=review_id).first()

        if comment_id is not "":
            comment = Comment.objects.filter(id=comment_id).first()
        else:
            comment = None
        if review is not None:
            comment = Comment(
                user=request.user,
                review=review,
                description=description,
                reply=comment,
            )
            comment.save()

            restaurant = review.restaurant
            reviews = Review.objects.filter(
                restaurant=restaurant).order_by("-pk")
            content = {
                'reviews': reviews
            }
            return render(request, "pizza_home/review.html", content)
        else:
            raise Http404("review id is not valid")
    else:
        return JsonResponse({"is_not_authenticated": True}, status=200)


def restaurant_rate(request):
    restaurant_id = request.GET.get('restaurant_id')

    reviews = Review.objects.filter(restaurant_id=restaurant_id)
    avg_rate = average_rating(reviews)
    review_count = reviews.count()

    response = JsonResponse({
        'review_count': review_count,
        'avg_rate': avg_rate,
    }, status=200)

    return response
