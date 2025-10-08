# 代码生成时间: 2025-10-09 03:11:34
import json
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

"""
Django application component for a governance token system.
This module includes models for tokens and transactions,
as well as views to handle token management and transaction operations.
"""

class Token(models.Model):
    """
    A model representing a governance token.
    """
    name = models.CharField(max_length=255, unique=True, help_text="The name of the token.")
    total_supply = models.DecimalField(max_digits=30, decimal_places=8, help_text="The total supply of the token.")
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, help_text="The owner of the token.")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        """
        Additional options for the Token model.
        """

class Transaction(models.Model):
    """
    A model representing a token transaction.
    """
    token = models.ForeignKey(Token, on_delete=models.CASCADE, help_text="The token involved in the transaction.")
    sender = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="sent_transactions", help_text="The sender of the transaction.")
    recipient = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="received_transactions", help_text="The recipient of the transaction.")
    amount = models.DecimalField(max_digits=30, decimal_places=8, help_text="The amount of tokens transferred.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The timestamp of the transaction.")
    
    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}: {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        """
        Additional options for the Transaction model.
        """

class TokenView(View):
    """
    A view to handle token management.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Create a new token.
        """
        try:
            data = json.loads(request.body)
            name = data.get("name")
            total_supply = data.get("total_supply")
            if not name or not total_supply:
                return JsonResponse({'error': 'Missing token name or total supply.'}, status=400)
            new_token = Token.objects.create(name=name, total_supply=total_supply, owner=request.user)
            return JsonResponse({'message': 'Token created successfully.', 'token_id': new_token.id}, status=201)
        except (ValueError, KeyError):
            return JsonResponse({'error': 'Invalid request data.'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'A token with this name already exists.'}, status=409)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, token_id=None):
        """
        Retrieve a token or all tokens.
        """
        try:
            if token_id:
                token = Token.objects.get(id=token_id)
                return JsonResponse({'token': {'id': token.id, 'name': token.name, 'total_supply': token.total_supply, 'owner': token.owner.username}})
            else:
                tokens = Token.objects.all()
                return JsonResponse({'tokens': [{'id': token.id, 'name': token.name, 'total_supply': token.total_supply, 'owner': token.owner.username} for token in tokens]}, status=200)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class TransactionView(View):
    """
    A view to handle token transactions.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Initiate a token transaction.
        """
        try:
            data = json.loads(request.body)
            token_id = data.get("token_id\)
            sender_id = data.get("sender_id\)
            recipient_id = data.get("recipient_id\)
            amount = data.get("amount\)
            if not token_id or not sender_id or not recipient_id or not amount:
                return JsonResponse({'error': 'Missing transaction data.'}, status=400)
            token = Token.objects.get(id=token_id)
            sender = token.owner  # Assuming the sender is the token owner for simplicity
            recipient = User.objects.get(id=recipient_id)
            if sender == recipient:
                return JsonResponse({'error': 'Sender and recipient cannot be the same.'}, status=400)
            transaction = Transaction.objects.create(token=token, sender=sender, recipient=recipient, amount=amount)
            return JsonResponse({'message': 'Transaction completed successfully.', 'transaction_id': transaction.id}, status=201)
        except (ValueError, KeyError):
            return JsonResponse({'error': 'Invalid request data.'}, status=400)
        except (Token.DoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'Token or user not found.'}, status=404)
        except ValidationError:
            return JsonResponse({'error': 'Invalid transaction amount.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

urlpatterns = [
    path('token/', TokenView.as_view(), name='token_view'),
    path('transaction/', TransactionView.as_view(), name='transaction_view'),
]
