from urllib import response
from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from movies.models import Movie

from .serializers import CustomUserSerializer, MovieCommentSerializer, CustomUserDetailSerializer
from .models import CustomUser, MovieScore, MovieComment


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all().order_by('id')

    def update(self, request, *args, **kwargs):
        customuser = self.get_object()
        if 'username' in request.data:
            customuser.username = request.data['username']
        if 'biography' in request.data:
            customuser.biography = request.data['biography']
        if 'website' in request.data:
            customuser.website = request.data['website']
        if 'avatar' in request.data:
            customuser.avatar = request.data['avatar']
        if 'role' in request.data:
            customuser.role = request.data['role']
        customuser.save()
        serializer = CustomUserSerializer(customuser)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def calculateMovieScore(movie):
    score_list = MovieScore.objects.filter(movie=movie)
    if (score_list.count() == 0):
        movie.avg_score = 0
        movie.score_count = 0
    else:
        sum = 0
        for item in score_list:
            sum += item.score
        avg = round((sum / score_list.count()) * 10)
        movie.avg_score = avg
        movie.score_count = score_list.count()
    movie.save()


class CustomUserDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserDetailSerializer
    queryset = CustomUser.objects.all().order_by('id')

    def update(self, request, *args, **kwargs):
        customuser = self.get_object()
        if 'movie' in request.data:
            movie = Movie.objects.get(id=int(request.data['movie']))
            if 'like' in request.data:
                if movie in customuser.movies_like.all():
                    customuser.movies_like.remove(movie)
                    movie.like_count -= 1
                else:
                    customuser.movies_like.add(movie)
                    movie.like_count += 1
            if 'watched' in request.data:
                if movie in customuser.movies_watched.all():
                    customuser.movies_watched.remove(movie)
                    movie.watched_count -= 1
                else:
                    customuser.movies_watched.add(movie)
                    movie.watched_count += 1
            if 'watchlist' in request.data:
                if movie in customuser.movies_watchlist.all():
                    customuser.movies_watchlist.remove(movie)
                    movie.watchlist_count -= 1
                else:
                    customuser.movies_watchlist.add(movie)
                    movie.watchlist_count += 1
            if 'score' in request.data:
                score = int(request.data['score'])
                exists = False
                for item in customuser.movies_rated.all():
                    if item.movie == movie:
                        exists = True
                        if score > 0:
                            # Update
                            item.score = score
                            item.save()
                        else:
                            # Delete
                            customuser.movies_rated.remove(item)
                            MovieScore.objects.filter(id=item.id).delete()
                if exists is False:
                    # Create
                    item = MovieScore.objects.create(movie=movie, score=score)
                    customuser.movies_rated.add(item)
                # Calculate Score
                calculateMovieScore(movie)
        customuser.save()
        serializer = CustomUserDetailSerializer(customuser)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class MovieCommentPagination(pagination.PageNumberPagination):
    page_size = 40


class MovieCommentViewSet(viewsets.ModelViewSet):
    serializer_class = MovieCommentSerializer
    queryset = MovieComment.objects.all().order_by('-like_count', '-created_at')
    pagination_class = MovieCommentPagination

    def get_queryset(self):
        queryset = MovieComment.objects.all().order_by('-like_count', '-created_at')
        movie = self.request.query_params.get('movie', None)
        order = self.request.query_params.get('order', None)
        if movie is not None:
            queryset = queryset.filter(
                movie__id=int(movie)).distinct()
        if order is not None:
            queryset = queryset.order_by(order).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        movie = Movie.objects.get(id=int(request.data['movie']))
        spoiler_alert = False
        if 'spoiler_alert' in request.data:
            spoiler_alert = True
        score = 0
        score_obj = user.movies_rated.filter(movie=movie)
        if score_obj:
            score = score_obj[0].score
        movieComment = MovieComment.objects.create(
            movie=movie,
            user=user,
            comment=request.data['comment'],
            spoiler_alert=spoiler_alert,
            score=score
        )
        serializer = MovieCommentSerializer(movieComment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        movieComment = self.get_object()
        movieComment.comment = response.data['comment']
        movieComment.save()
        serializer = MovieCommentSerializer(movieComment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'http://localhost:3000/'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/'
    client_class = OAuth2Client
