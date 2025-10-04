# 代码生成时间: 2025-10-04 19:45:50
from django.db import models
from django.views.generic import ListView
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
import json

# Models.py
def NFTModel(models.Model):
    """Model for Non-Fungible Token (NFT)"""
    class Meta:
        db_table = 'nft'
    
    name = models.CharField(max_length=255, help_text="NFT's name")
    description = models.TextField(help_text="NFT's description")
    image_url = models.URLField(help_text="URL of NFT's image")
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text="Owner of NFT")

    def __str__(self):
        return self.name

# Views.py
@require_http_methods(["POST"])
def mint_nft(request):
    """Endpoint to mint a new NFT"""
    data = json.loads(request.body)
    try:
        nft = NFTModel.objects.create(
            name=data['name'],
            description=data['description'],
            image_url=data['image_url'],
            owner=request.user
        )
        return JsonResponse({'message': 'NFT minted successfully', 'nft_id': nft.id})
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {e}'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    class NFTListView(ListView):
        """List view for displaying all NFTs"""
        model = NFTModel
        template_name = 'nft_list.html'
        context_object_name = 'nfts'

# urls.py
urlpatterns = [
    path('mints/', mint_nft, name='mint_nft'),
    path('nfts/', NFTListView.as_view(), name='nft_list'),
]
